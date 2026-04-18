"""
Preference Tracker — theo dõi và lưu sở thích người dùng.
Requirements: 8.1 - 8.6
"""
import json
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

MIN_INTERACTIONS = 3
import os
from dotenv import load_dotenv
load_dotenv()
HAIKU_MODEL = os.getenv("HAIKU_MODEL") or os.getenv("MODEL", "claude-sonnet-4.6")


@dataclass
class UserPreferences:
    language: str = "vi"
    response_length: str = "medium"  # short | medium | long
    format: str = "markdown"         # markdown | plain
    interaction_count: int = 0


def _detect_language(text: str) -> str:
    """Phát hiện ngôn ngữ đơn giản dựa trên ký tự."""
    try:
        # Thử dùng langdetect nếu có
        import langdetect
        return langdetect.detect(text)
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback: kiểm tra ký tự tiếng Việt
    vietnamese_chars = set("àáâãèéêìíòóôõùúýăđơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ")
    text_lower = text.lower()
    vi_count = sum(1 for c in text_lower if c in vietnamese_chars)
    if vi_count > 2:
        return "vi"
    return "en"


def detect_preferences(message: str, response_length: int) -> dict:
    """Phát hiện preferences từ message và độ dài response."""
    prefs = {}

    # Ngôn ngữ
    prefs["language"] = _detect_language(message)

    # Độ dài response
    if response_length < 200:
        prefs["response_length"] = "short"
    elif response_length < 800:
        prefs["response_length"] = "medium"
    else:
        prefs["response_length"] = "long"

    return prefs


def load_preferences(memory_store) -> UserPreferences:
    """Load preferences từ memory store."""
    try:
        results = memory_store.search_memory("user_preference", n_results=3)
        for r in results:
            if r.get("metadata", {}).get("category") == "user_preference":
                data = json.loads(r["content"])
                return UserPreferences(**{k: v for k, v in data.items() if k in UserPreferences.__dataclass_fields__})
    except Exception as e:
        logger.debug(f"Could not load preferences: {e}")
    return UserPreferences()


def save_preferences(prefs: UserPreferences, memory_store) -> None:
    """Lưu preferences vào memory, overwrite cũ."""
    try:
        # Xóa preference cũ
        existing = memory_store.search_memory("user_preference", n_results=5)
        for r in existing:
            if r.get("metadata", {}).get("category") == "user_preference":
                doc_id = r.get("id", "")
                if doc_id:
                    memory_store.delete_memory(doc_id)
        # Lưu mới
        memory_store.save_memory(
            json.dumps(asdict(prefs)),
            {"category": "user_preference"}
        )
    except Exception as e:
        logger.warning(f"Could not save preferences: {e}")


def build_preference_prompt(prefs: UserPreferences) -> str:
    """Tạo đoạn text inject vào system prompt."""
    if prefs.interaction_count < MIN_INTERACTIONS:
        return ""
    lang_map = {"vi": "tiếng Việt", "en": "English"}
    lang = lang_map.get(prefs.language, prefs.language)
    length_map = {"short": "ngắn gọn", "medium": "vừa phải", "long": "chi tiết"}
    length = length_map.get(prefs.response_length, "vừa phải")
    fmt = "markdown (dùng headers, bullets)" if prefs.format == "markdown" else "plain text"
    vi_extra = " — tiếng Việt chuẩn chính tả, đầy đủ dấu thanh" if prefs.language == "vi" else ""
    return f"\n\n[Sở thích người dùng: Trả lời bằng {lang}{vi_extra}, độ dài {length}, format {fmt}]"
