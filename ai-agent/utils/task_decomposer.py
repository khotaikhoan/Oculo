"""
Task Decomposer — phân tách task phức tạp thành subtasks bằng Haiku.
Requirements: 6.1 - 6.6
"""
import logging
import os
import re
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

_MAIN_MODEL = os.getenv("MODEL", "claude-sonnet-4-5")
HAIKU_MODEL = os.getenv("HAIKU_MODEL") or _MAIN_MODEL
MAX_SUBTASKS = 6
WORD_THRESHOLD = 140  # ít gọi Haiku phân tách → bớt latency mỗi lượt chat

# Pattern multi-step rõ ràng → decompose dù dưới WORD_THRESHOLD
_MULTISTEP_RE = re.compile(
    r'(và sau đó|sau khi|tiếp theo|cuối cùng|bước \d|step \d'
    r'|rồi.*(?:và|rồi)'
    r'|(?:tìm|search|nghiên cứu|tổng hợp).*(?:lưu|tạo|ghi|viết)'
    r'|\d+\.\s\w)',
    re.IGNORECASE | re.DOTALL,
)

# Patterns cho thấy task KHÔNG cần decompose (câu hỏi đơn giản)
_SIMPLE_PATTERNS = re.compile(
    r'^(xin chào|hello|hi|hey|chào|cảm ơn|thanks|thank you'
    r'|giải thích|explain|định nghĩa|define|là gì|what is|nghĩa là'
    r'|dịch|translate|tóm tắt|summarize|viết lại|rewrite|format'
    r'|bao nhiêu|how many|how much|khi nào|when|tại sao|why'
    r'|thời tiết|weather|giờ mấy|what time)',
    re.IGNORECASE,
)


def _is_multistep(task: str) -> bool:
    """Phát hiện nhanh task có nhiều bước mà không cần đếm từ."""
    return bool(_MULTISTEP_RE.search(task))


def _is_simple(task: str) -> bool:
    """Phát hiện task đơn giản không cần decompose."""
    return bool(_SIMPLE_PATTERNS.match(task.strip()))


@dataclass
class SubTask:
    index: int
    description: str
    status: str = "pending"  # pending | running | done | failed
    result: str = ""


def decompose_task(task: str, anthropic_client) -> list[str]:
    """
    Phân tách task phức tạp thành subtasks.
    Trả về list rỗng nếu task đơn giản.
    """
    word_count = len(task.split())

    # Bỏ qua nếu task đơn giản
    if _is_simple(task):
        return []

    # Chỉ decompose nếu đủ phức tạp
    if word_count <= WORD_THRESHOLD and not _is_multistep(task):
        return []

    try:
        user_msg = (
            f"Chia task sau thành {MAX_SUBTASKS} subtasks ngắn gọn tối đa, "
            f"mỗi subtask 1 dòng, bắt đầu bằng số thứ tự (1. 2. 3. ...):\n\n{task}"
        )
        r = anthropic_client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": user_msg}],
        )
        text_out = next((b.text for b in r.content if getattr(b, "type", None) == "text"), "")
        if not text_out:
            return []
        lines = text_out.strip().split("\n")
        subtasks = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            cleaned = line.lstrip("0123456789.-) ").strip()
            if cleaned:
                subtasks.append(cleaned)
        return subtasks[:MAX_SUBTASKS]
    except Exception as e:
        logger.warning(f"Task decomposition failed: {e}")
        return []
