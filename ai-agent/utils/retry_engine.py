"""
Retry Engine — exponential backoff với full jitter, per-category config.
Tách biệt hoàn toàn khỏi fallback logic.
"""
import time
import random
import logging
from typing import Callable, Optional

from utils.error_classifier import ErrorClassifier, ErrorCategory, ClassifiedError

logger = logging.getLogger("oculo.retry")


class RetryConfig:
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0,
                 max_delay: float = 60.0, exponential_base: float = 2.0,
                 jitter: bool = True):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exp_base = exponential_base
        self.jitter = jitter


# Config riêng cho từng category
RETRY_CONFIGS: dict[ErrorCategory, RetryConfig] = {
    ErrorCategory.TRANSIENT_RATE_LIMIT: RetryConfig(
        max_attempts=4, base_delay=30.0, max_delay=120.0,
        exponential_base=1.5, jitter=True),
    ErrorCategory.TRANSIENT_OVERLOAD: RetryConfig(
        max_attempts=3, base_delay=10.0, max_delay=60.0,
        exponential_base=2.0, jitter=True),
    ErrorCategory.TRANSIENT_NETWORK: RetryConfig(
        max_attempts=3, base_delay=2.0, max_delay=30.0,
        exponential_base=2.0, jitter=True),
    ErrorCategory.TRANSIENT_LOCK: RetryConfig(
        max_attempts=5, base_delay=0.5, max_delay=10.0,
        exponential_base=1.5, jitter=True),
    ErrorCategory.TRANSIENT_RENDERING: RetryConfig(
        max_attempts=3, base_delay=2.0, max_delay=10.0,
        exponential_base=1.5, jitter=False),
    # Recoverable — 1-2 attempts rồi chuyển fallback
    ErrorCategory.RECOVERABLE_ELEMENT_NOT_FOUND: RetryConfig(
        max_attempts=2, base_delay=1.5, max_delay=5.0,
        exponential_base=2.0, jitter=False),
    ErrorCategory.RECOVERABLE_NAVIGATION_FAILED: RetryConfig(
        max_attempts=2, base_delay=3.0, max_delay=10.0,
        exponential_base=2.0, jitter=True),
    ErrorCategory.RECOVERABLE_AUTH_EXPIRED: RetryConfig(
        max_attempts=1),
    ErrorCategory.RECOVERABLE_CONTENT_CHANGED: RetryConfig(
        max_attempts=2, base_delay=1.0, max_delay=5.0,
        exponential_base=2.0, jitter=False),
    # Fatal — không retry
    ErrorCategory.FATAL_PERMISSION_DENIED: RetryConfig(max_attempts=1),
    ErrorCategory.FATAL_CAPTCHA_BLOCK:     RetryConfig(max_attempts=1),
    ErrorCategory.FATAL_INVALID_API_KEY:   RetryConfig(max_attempts=1),
    ErrorCategory.FATAL_QUOTA_EXCEEDED:    RetryConfig(max_attempts=1),
    ErrorCategory.FATAL_FILE_NOT_EXIST:    RetryConfig(max_attempts=1),
    ErrorCategory.FATAL_SYSTEM_CRASH:      RetryConfig(max_attempts=1),
}

_DEFAULT_CONFIG = RetryConfig(max_attempts=2, base_delay=1.0)

# Vision tools: chỉ retry 1 lần — nếu fail chuyển ngay sang DOM tools
_VISION_TOOLS = {"browser_analyze_page", "browser_vision_click", "browser_vision_type", "screenshot_and_analyze"}
_VISION_CONFIG = RetryConfig(max_attempts=1)


def compute_delay(config: RetryConfig, attempt: int,
                  retry_after: Optional[float] = None) -> float:
    """Exponential backoff với full jitter — tránh thundering herd."""
    if retry_after is not None:
        return max(0.0, float(retry_after))  # respect API's Retry-After header
    delay = config.base_delay * (config.exp_base ** (attempt - 1))
    delay = min(delay, config.max_delay)
    if config.jitter:
        delay = random.uniform(0, delay)  # full jitter
    return delay


def run_with_retry(
    tool_fn: Callable,
    tool_name: str,
    tool_input: dict,
    yield_fn: Optional[Callable] = None,
) -> dict:
    """
    Chạy tool_fn với retry thông minh theo error category.

    Args:
        tool_fn: callable(**tool_input) → str result
        tool_name: tên tool để classify + log
        tool_input: dict input cho tool
        yield_fn: optional callback(event_dict) để emit SSE event

    Returns dict:
        {
          "success": bool,
          "result": str | None,
          "attempts": int,
          "error": ClassifiedError | None,
          "should_fallback": bool,
          "should_abort": bool,
        }
    """
    attempt = 0
    last_classified: Optional[ClassifiedError] = None

    while True:
        attempt += 1
        try:
            result = tool_fn(**tool_input)
            # Kiểm tra error string từ run_tool() (trả về "Error: ..." thay vì raise)
            if isinstance(result, str) and (
                result.startswith("Error:") or result.startswith("Lỗi:")
            ):
                raise RuntimeError(result)

            if attempt > 1:
                logger.info(f"{tool_name} succeeded on attempt {attempt}")
            return {
                "success": True,
                "result": result,
                "attempts": attempt,
                "error": None,
                "should_fallback": False,
                "should_abort": False,
            }

        except Exception as exc:
            classified = ErrorClassifier.classify(exc, tool_name, tool_input)
            last_classified = classified
            logger.warning(
                f"Tool {tool_name} failed (attempt {attempt}): "
                f"{classified.category.value} — {exc}"
            )

            config = RETRY_CONFIGS.get(classified.category, _DEFAULT_CONFIG)
            # Vision tools: không retry — chuyển ngay sang fallback/DOM tools
            if tool_name in _VISION_TOOLS:
                config = _VISION_CONFIG

            # Fatal → abort ngay, không retry
            if classified.is_fatal():
                logger.error(f"Fatal error on {tool_name}: {exc}")
                return {
                    "success": False,
                    "result": None,
                    "attempts": attempt,
                    "error": classified,
                    "should_fallback": False,
                    "should_abort": True,
                }

            # Hết attempts → chuyển fallback nếu có
            if attempt >= config.max_attempts:
                has_fallback = bool(classified.suggested_fallback)
                logger.warning(
                    f"{tool_name} exhausted {attempt} attempts. "
                    f"Fallback: {classified.suggested_fallback}"
                )
                return {
                    "success": False,
                    "result": None,
                    "attempts": attempt,
                    "error": classified,
                    "should_fallback": has_fallback,
                    "should_abort": not has_fallback,
                }

            # Tính delay và notify frontend
            delay = compute_delay(config, attempt, classified.retry_after_sec)
            if yield_fn:
                try:
                    yield_fn({
                        "type": "retry_attempt",
                        "tool": tool_name,
                        "attempt": attempt,
                        "max_attempts": config.max_attempts,
                        "delay_sec": round(delay, 1),
                        "reason": classified.user_message,
                        "category": classified.category.value,
                    })
                except Exception:
                    pass

            logger.info(
                f"Retrying {tool_name} in {delay:.1f}s "
                f"(attempt {attempt + 1}/{config.max_attempts})"
            )
            time.sleep(delay)
