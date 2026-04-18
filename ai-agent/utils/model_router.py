"""
Model Router — phân loại task và chọn model phù hợp.
Simple tasks → HAIKU_MODEL (mặc định = MODEL nếu không khai báo), Complex → MODEL
Requirements: 11.1 - 11.6
"""
from dataclasses import dataclass

import os
from dotenv import load_dotenv
load_dotenv()

_DEFAULT = os.getenv("MODEL", "claude-sonnet-4-5")
# Haiku cho routing: ưu tiên HAIKU_MODEL; nếu không set thì dùng MODEL (tránh model không tồn tại trên proxy).
HAIKU_MODEL  = os.getenv("HAIKU_MODEL") or _DEFAULT
SONNET_MODEL = _DEFAULT

# Nếu HAIKU_MODEL == SONNET_MODEL thì không cần routing — luôn dùng 1 model
_ROUTING_ENABLED = (HAIKU_MODEL != SONNET_MODEL)

SIMPLE_KEYWORDS = {
    "xin chào", "hello", "hi", "hey", "cảm ơn", "thanks", "thank you",
    "tóm tắt ngắn", "format", "dịch", "translate", "giải thích ngắn",
    "là gì", "what is", "định nghĩa", "define",
}

COMPLEX_KEYWORDS = {
    "viết code", "lập trình", "code", "script", "phân tích", "analyze",
    "tìm kiếm", "search", "tải", "download", "cài đặt", "install",
    "chạy", "run", "mở", "open", "tạo file", "create file", "xóa",
    "delete", "di chuyển", "move", "copy", "sao chép", "kiểm tra",
    "check", "monitor", "theo dõi", "screenshot", "chụp màn hình",
    "browser", "web", "url", "http",
}


@dataclass
class ModelRoutingDecision:
    model: str
    complexity: str  # "simple" | "complex" | "user_specified"
    reason: str


def route_model(
    message: str,
    has_tool_history: bool = False,
    user_specified_model: str = None,
) -> ModelRoutingDecision:
    """Chọn model phù hợp dựa trên độ phức tạp của task."""
    if user_specified_model:
        return ModelRoutingDecision(
            model=user_specified_model,
            complexity="user_specified",
            reason="user override",
        )

    # Nếu HAIKU = SONNET thì không route — tránh nhầm model gây mất dấu tiếng Việt
    if not _ROUTING_ENABLED:
        return ModelRoutingDecision(
            model=SONNET_MODEL,
            complexity="complex",
            reason="routing disabled (HAIKU_MODEL == MODEL)",
        )

    msg_lower = message.lower()
    word_count = len(message.split())

    # Có tool history: câu tiếp theo ngắn / đơn giản → Haiku (nhanh hơn Sonnet giữa các tool).
    if has_tool_history:
        if any(kw in msg_lower for kw in SIMPLE_KEYWORDS):
            return ModelRoutingDecision(
                model=HAIKU_MODEL,
                complexity="simple",
                reason="simple reply in tool session",
            )
        if word_count <= 22 and not any(kw in msg_lower for kw in COMPLEX_KEYWORDS):
            return ModelRoutingDecision(
                model=HAIKU_MODEL,
                complexity="simple",
                reason="short follow-up in tool session",
            )
        return ModelRoutingDecision(
            model=SONNET_MODEL,
            complexity="complex",
            reason="has tool history",
        )

    # Complex nếu message dài hoặc có complex keywords
    if word_count > 30:
        return ModelRoutingDecision(
            model=SONNET_MODEL,
            complexity="complex",
            reason=f"long message ({word_count} words)",
        )

    if any(kw in msg_lower for kw in COMPLEX_KEYWORDS):
        matched = next(kw for kw in COMPLEX_KEYWORDS if kw in msg_lower)
        return ModelRoutingDecision(
            model=SONNET_MODEL,
            complexity="complex",
            reason=f"complex keyword: {matched}",
        )

    # Simple nếu có simple keywords
    if any(kw in msg_lower for kw in SIMPLE_KEYWORDS):
        matched = next(kw for kw in SIMPLE_KEYWORDS if kw in msg_lower)
        return ModelRoutingDecision(
            model=HAIKU_MODEL,
            complexity="simple",
            reason=f"simple keyword: {matched}",
        )

    # Default: Sonnet để an toàn
    return ModelRoutingDecision(
        model=SONNET_MODEL,
        complexity="complex",
        reason="default safe choice",
    )
