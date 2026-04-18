"""Trích văn bản thuần từ `content` trả về của Anthropic Messages API."""


def text_from_anthropic_content(content: list) -> str:
    parts: list[str] = []
    for block in content:
        if isinstance(block, dict):
            if block.get("type") == "text":
                parts.append(block.get("text", ""))
        elif getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", ""))
    return "".join(parts).strip()
