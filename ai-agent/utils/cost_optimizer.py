"""
Cost Optimizer — tối ưu chi phí API Anthropic.

1. Prompt caching — cache_control cho system prompt tĩnh (tiết kiệm 90% input tokens)
2. Tool filtering — bỏ TOOLS list khi task không cần tool
3. Memory threshold — chỉ inject memory khi similarity score > MIN_MEMORY_SCORE
4. Lazy self-correction — chỉ verify khi đáng verify
5. Token counter — đếm và yield token usage
"""
import re
from typing import Optional

# ── 1. Prompt Caching ──────────────────────────────────────────────────────────

def build_cached_system(static_part: str, dynamic_part: str = "") -> list[dict]:
    """
    Tạo system prompt với cache_control cho phần tĩnh.
    Anthropic cache_control: phần static được cache, tiết kiệm ~90% input tokens.
    Yêu cầu: static_part >= 1024 tokens (~800 từ).
    """
    blocks = [
        {
            "type": "text",
            "text": static_part,
            "cache_control": {"type": "ephemeral"},
        }
    ]
    if dynamic_part and dynamic_part.strip():
        blocks.append({"type": "text", "text": dynamic_part})
    return blocks


# ── 2. Tool Filtering ──────────────────────────────────────────────────────────

# Patterns cho thấy task KHÔNG cần tool
NO_TOOL_PATTERNS = [
    r"^(xin chào|hello|hi|hey|chào)\b",
    r"^(cảm ơn|thanks|thank you)\b",
    r"\b(giải thích|explain|định nghĩa|define|là gì|what is|nghĩa là)\b",
    r"^(dịch|translate)\s+.{1,100}$",
    r"^(tóm tắt|summarize|summary)\s+.{1,200}$",
    r"^(viết lại|rewrite|format|sửa lỗi chính tả)\s+",
    r"^(bao nhiêu|how many|how much|khi nào|when|tại sao|why|như thế nào|how)\b",
]

# Patterns cho thấy task CẦN tool
NEEDS_TOOL_PATTERNS = [
    r"\b(mở|open|chạy|run|tải|download|cài|install)\b",
    r"\b(file|folder|thư mục|desktop|terminal)\b",
    r"(https?://|\b(browser|web|url|google|tìm kiếm|search)\b)",
    r"\b(screenshot|chụp màn hình|màn hình)\b",
    r"\b(nhớ|remember|lưu|save|ghi nhớ)\b",
    r"\b(kiểm tra|check|xem|monitor|theo dõi)\b",
    r"\b(tạo|create|viết file|write file|xóa|delete)\b",
    r"\b(cpu|ram|disk|memory|process|pid)\b",
]


def should_use_tools(message: str, has_tool_history: bool) -> bool:
    """Quyết định có gửi TOOLS list lên API không."""
    if has_tool_history:
        return True

    msg_lower = message.lower()

    # Nếu có pattern cần tool → dùng tool
    for pattern in NEEDS_TOOL_PATTERNS:
        if re.search(pattern, msg_lower):
            return True

    # Nếu có pattern không cần tool → bỏ tool
    for pattern in NO_TOOL_PATTERNS:
        if re.search(pattern, msg_lower):
            return False

    # Message dài thường cần tool
    if len(message.split()) > 20:
        return True

    # Default: dùng tool để an toàn
    return True


# ── 3. Memory Threshold ────────────────────────────────────────────────────────

MIN_MEMORY_SCORE = 0.72  # Chỉ inject memory có similarity >= 72%
MAX_MEMORY_TOKENS = 400  # Giới hạn tổng token memory inject


def filter_memories(memories: list[dict], max_tokens: int = MAX_MEMORY_TOKENS) -> list[dict]:
    """
    Lọc memories theo similarity score và giới hạn token.
    memories: list of {"content": str, "distance": float, ...}
    distance thấp = similarity cao (ChromaDB cosine distance).
    """
    # Lọc theo threshold (distance < 1 - MIN_MEMORY_SCORE)
    threshold = 1.0 - MIN_MEMORY_SCORE

    def _dist(m):
        d = m.get("distance")
        return d if isinstance(d, (int, float)) else 1.0

    filtered = [m for m in memories if _dist(m) <= threshold]

    # Giới hạn token (ước tính 1 token ≈ 4 chars)
    result = []
    total_chars = 0
    for m in filtered:
        content = m.get("content", "")
        if total_chars + len(content) > max_tokens * 4:
            break
        result.append(m)
        total_chars += len(content)

    return result


def build_memory_context(memories: list[dict]) -> str:
    """Tạo memory context string từ filtered memories."""
    if not memories:
        return ""
    lines = ["[Relevant memories:]"]
    for m in memories:
        ts = m.get("metadata", {}).get("timestamp", "")[:10]
        score = round(1.0 - m.get("distance", 0.5), 2)
        lines.append(f"- [{ts}] ({score}) {m.get('content', '')}")
    return "\n".join(lines)


# ── 4. Lazy Self-Correction ────────────────────────────────────────────────────

MIN_FILE_SIZE_FOR_VERIFY = 500   # bytes — chỉ verify file > 500 chars
IMPORTANT_DOMAINS = {
    "github.com", "google.com", "youtube.com", "facebook.com",
    "twitter.com", "x.com", "linkedin.com", "amazon.com",
}


def should_verify_write(path: str, content: str) -> bool:
    """Chỉ verify write_file khi file đủ quan trọng."""
    if len(content) < MIN_FILE_SIZE_FOR_VERIFY:
        return False
    # Verify các file code/config quan trọng
    important_exts = {".py", ".js", ".ts", ".json", ".yaml", ".yml", ".sh", ".md"}
    ext = "." + path.rsplit(".", 1)[-1].lower() if "." in path else ""
    return ext in important_exts


def should_verify_navigate(url: str) -> bool:
    """Chỉ verify browser_navigate cho các domain quan trọng."""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.lower().replace("www.", "")
        return domain in IMPORTANT_DOMAINS
    except Exception:
        return False


# ── 5. Token Counter ───────────────────────────────────────────────────────────

class TokenUsageTracker:
    """Track token usage trong session."""

    def __init__(self):
        self.input_tokens = 0
        self.output_tokens = 0
        self.cache_read_tokens = 0
        self.cache_write_tokens = 0
        self.api_calls = 0

    def update(self, usage):
        """Update từ Anthropic response.usage hoặc OpenAI (prompt/completion tokens)."""
        if usage is None:
            return

        def _int(v, fallback=0):
            try:
                return int(v) if v is not None else fallback
            except (TypeError, ValueError):
                return fallback

        inp = getattr(usage, "input_tokens", None)
        if inp is None:
            inp = getattr(usage, "prompt_tokens", None)
        outp = getattr(usage, "output_tokens", None)
        if outp is None:
            outp = getattr(usage, "completion_tokens", None)
        self.input_tokens += _int(inp)
        self.output_tokens += _int(outp)
        self.cache_read_tokens  += _int(getattr(usage, "cache_read_input_tokens", 0))
        self.cache_write_tokens += _int(getattr(usage, "cache_creation_input_tokens", 0))
        self.api_calls += 1

    def estimate_cost_usd(self, model: str) -> float:
        """Ước tính chi phí USD (giá tháng 4/2026)."""
        # Claude Sonnet 4.5 / claude-sonnet-4-5
        if "sonnet" in model:
            input_cost  = self.input_tokens  * 3.0  / 1_000_000
            output_cost = self.output_tokens * 15.0 / 1_000_000
            cache_read  = self.cache_read_tokens  * 0.30 / 1_000_000
            cache_write = self.cache_write_tokens * 3.75 / 1_000_000
        # Claude Haiku 4.5 / claude-haiku-4-5
        elif "haiku" in model:
            input_cost  = self.input_tokens  * 0.80 / 1_000_000
            output_cost = self.output_tokens * 4.0  / 1_000_000
            cache_read  = self.cache_read_tokens  * 0.08 / 1_000_000
            cache_write = self.cache_write_tokens * 1.0  / 1_000_000
        # Claude Opus 4 / claude-opus-4
        elif "opus" in model:
            input_cost  = self.input_tokens  * 15.0 / 1_000_000
            output_cost = self.output_tokens * 75.0 / 1_000_000
            cache_read  = self.cache_read_tokens  * 1.50 / 1_000_000
            cache_write = self.cache_write_tokens * 18.75 / 1_000_000
        # Gemini / OpenAI-compat — ước tính chung
        else:
            input_cost  = self.input_tokens  * 1.0  / 1_000_000
            output_cost = self.output_tokens * 3.0  / 1_000_000
            cache_read  = 0.0
            cache_write = 0.0
        return round(input_cost + output_cost + cache_read + cache_write, 6)

    def to_dict(self, model: str = "") -> dict:
        return {
            "input_tokens":       self.input_tokens,
            "output_tokens":      self.output_tokens,
            "cache_read_tokens":  self.cache_read_tokens,
            "cache_write_tokens": self.cache_write_tokens,
            "api_calls":          self.api_calls,
            "estimated_cost_usd": self.estimate_cost_usd(model),
        }
