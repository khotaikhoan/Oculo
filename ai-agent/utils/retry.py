"""
Tool Retry Logic — tự động retry với exponential backoff khi tool thất bại.
Requirements: 2.1 - 2.5
"""
import time
import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)

RETRYABLE_TOOLS = {
    "run_shell",
    "browser_navigate",
    "browser_evaluate",
    "browser_fill",
    "browser_click",
    "browser_scroll",
    "browser_wait_for_human",
    "browser_analyze_page",
    "browser_vision_click",
    "browser_vision_type",
}
MAX_RETRIES = 3
BACKOFF_BASE = 1.0  # seconds: 1s, 2s, 4s


def is_error_result(result) -> bool:
    """Kiểm tra kết quả có phải lỗi không."""
    if result is None:
        return True
    s = result if isinstance(result, str) else str(result)
    lower = s.lower()
    return lower.startswith("error") or lower.startswith("lỗi:") or lower.startswith("action error") or "traceback" in lower


def run_tool_with_retry(
    name: str,
    inputs: dict,
    run_tool_fn: Callable,
    yield_fn: Optional[Callable] = None,
    max_retries: int = MAX_RETRIES,
) -> str:
    """
    Chạy tool với retry logic.
    yield_fn: callable nhận dict event để stream về client.
    """
    if name not in RETRYABLE_TOOLS:
        return run_tool_fn(name, inputs)

    if max_retries < 1:
        return run_tool_fn(name, inputs)
    last_error = None
    for attempt in range(max_retries):
        try:
            result = run_tool_fn(name, inputs)
            if is_error_result(result):
                raise RuntimeError(result)
            return result
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                wait = BACKOFF_BASE * (2 ** attempt)
                if yield_fn:
                    yield_fn({
                        "type": "tool_retry",
                        "name": name,
                        "attempt": attempt + 1,
                        "reason": last_error[:200],
                        "wait_seconds": wait,
                    })
                logger.warning(f"Tool {name} failed (attempt {attempt+1}/{max_retries}): {last_error}. Retrying in {wait}s...")
                time.sleep(wait)

    return f"Error after {max_retries} retries: {last_error}"
