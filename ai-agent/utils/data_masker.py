"""Che thông tin nhạy cảm trong output trước khi hiển thị."""
import re

PATTERNS = [
    # API keys (sk-...)
    (re.compile(r'(sk-[a-zA-Z0-9]{20,})', re.I),
     lambda m: m.group(1)[:8] + '***' + m.group(1)[-4:]),
    # AWS Access Key IDs
    (re.compile(r'(AKIA[A-Z0-9]{16})', re.I),
     lambda m: m.group(1)[:8] + '***'),
    # Credit cards
    (re.compile(r'\b(\d{4})[- ]?(\d{4})[- ]?(\d{4})[- ]?(\d{4})\b'),
     lambda m: f"{m.group(1)} **** **** {m.group(4)}"),
    # Passwords in common patterns
    (re.compile(r'(password|passwd|pwd|secret|token)\s*[=:]\s*["\']?(\S{4,})["\']?', re.I),
     lambda m: f"{m.group(1)}=***"),
    # Private keys
    (re.compile(r'-----BEGIN [A-Z ]+PRIVATE KEY-----.*?-----END [A-Z ]+PRIVATE KEY-----', re.DOTALL),
     lambda m: '[PRIVATE KEY REDACTED]'),
]


def mask_sensitive(text) -> str:
    """Che thông tin nhạy cảm trong text."""
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def mask_with_flag(text) -> tuple[str, bool]:
    """Giống mask_sensitive nhưng trả về (text_đã_mask, có_thay_đổi)."""
    original = text if isinstance(text, str) else (str(text) if text is not None else "")
    masked = mask_sensitive(text)
    return masked, masked != original
