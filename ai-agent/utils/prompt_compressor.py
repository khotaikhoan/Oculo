"""
Prompt Compressor — nén lịch sử hội thoại dài bằng Haiku.
Khi history > 20 messages, tóm tắt messages cũ, giữ 4 gần nhất.
Requirements: 12.1 - 12.6
"""
import logging

logger = logging.getLogger(__name__)

COMPRESSION_THRESHOLD = 14
KEEP_RECENT = 4
import os
from dotenv import load_dotenv
load_dotenv()
_MAIN_MODEL = os.getenv("MODEL", "claude-sonnet-4-5")
HAIKU_MODEL = os.getenv("HAIKU_MODEL") or _MAIN_MODEL


def compress_history(messages: list, anthropic_client) -> tuple[list, dict]:
    """
    Nén lịch sử nếu vượt ngưỡng.
    Returns: (new_messages, compression_info)
    compression_info rỗng nếu không cần nén.
    """
    if len(messages) <= COMPRESSION_THRESHOLD:
        return messages, {}

    old_messages = messages[:-KEEP_RECENT]
    recent_messages = messages[-KEEP_RECENT:]

    # Tạo text để tóm tắt
    history_lines = []
    for m in old_messages:
        role = m.get("role", "unknown").upper()
        content = m.get("content", "")
        if isinstance(content, list):
            # Multi-part content (text/images/tool_result, ...)
            parts: list[str] = []
            for p in content:
                if not isinstance(p, dict):
                    continue
                pt = p.get("type")
                if pt == "text":
                    v = p.get("text", "")
                    if isinstance(v, str) and v.strip():
                        parts.append(v.strip())
                elif pt == "tool_result":
                    v = p.get("content", "")  # tool_result (Anthropic) stores output in "content"
                    if isinstance(v, str) and v.strip():
                        parts.append(v.strip())
            content = " ".join(parts) or "[complex content]"
        history_lines.append(f"{role}: {str(content)[:300]}")

    history_text = "\n".join(history_lines)

    try:
        user_msg = (
            f"Tóm tắt cuộc hội thoại sau trong tối đa 500 từ, "
            f"giữ lại các điểm quan trọng, quyết định đã đưa ra, và kết quả:\n\n{history_text}"
        )
        r = anthropic_client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=600,
            messages=[{"role": "user", "content": user_msg}],
        )
        summary = next((b.text for b in r.content if getattr(b, "type", None) == "text"), "")
        if not summary:
            return messages, {}
    except Exception as e:
        logger.warning(f"Prompt compression failed, keeping original history: {e}")
        return messages, {}

    summary_message = {
        "role": "user",
        "content": f"[Tóm tắt hội thoại trước:]\n{summary}"
    }

    new_messages = [summary_message] + recent_messages
    info = {
        "compressed_count": len(old_messages),
        "summary_length": len(summary.split()),
        "new_length": len(new_messages),
    }
    return new_messages, info
