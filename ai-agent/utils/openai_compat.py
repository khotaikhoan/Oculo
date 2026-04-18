"""Client OpenAI-compatible tùy chọn (Gemini / chiasegpu qua /v1/chat/completions)."""
from __future__ import annotations

import os
import time

from dotenv import load_dotenv

load_dotenv()

_client = None
_ids_cache: tuple[float, list[str]] | None = None
_CACHE_TTL = 60.0


def openai_compat_configured() -> bool:
    key = (os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_COMPAT_API_KEY") or "").strip()
    base = (os.getenv("GEMINI_BASE_URL") or os.getenv("OPENAI_COMPAT_BASE_URL") or "").strip()
    return bool(key and base)


def get_openai_compat_client():
    global _client
    if not openai_compat_configured():
        raise RuntimeError(
            "Thiếu GEMINI_API_KEY (hoặc OPENAI_COMPAT_API_KEY) và GEMINI_BASE_URL trong .env"
        )
    if _client is None:
        from openai import OpenAI

        key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_COMPAT_API_KEY")
        base = (os.getenv("GEMINI_BASE_URL") or os.getenv("OPENAI_COMPAT_BASE_URL")).rstrip("/")
        _client = OpenAI(api_key=key, base_url=base)
    return _client


def clear_openai_compat_model_cache() -> None:
    global _ids_cache
    _ids_cache = None


def list_openai_compat_model_ids() -> list[str]:
    """Gọi GET /v1/models trên base URL; thêm id từ GEMINI_EXTRA_MODELS."""
    global _ids_cache
    now = time.time()
    if _ids_cache is not None and (now - _ids_cache[0]) < _CACHE_TTL:
        return list(_ids_cache[1])

    ids: list[str] = []
    if openai_compat_configured():
        try:
            oai = get_openai_compat_client()
            ml = oai.models.list()
            ids = [getattr(m, "id", None) or (m.get("id") if isinstance(m, dict) else None) for m in ml]
            ids = [i for i in ids if i]
        except Exception:
            ids = []

    for raw in (os.getenv("GEMINI_EXTRA_MODELS") or "").split(","):
        p = raw.strip()
        if p and p not in ids:
            ids.append(p)
    gm = (os.getenv("GEMINI_MODEL") or "").strip()
    if gm and gm not in ids:
        ids.append(gm)

    _ids_cache = (now, ids)
    return list(ids)


def _is_claude_messages_style_id(model_id: str) -> bool:
    """Id dành cho Anthropic Messages API (kể cả dạng router prefix/model)."""
    core = model_id.split("/", 1)[-1] if "/" in model_id else model_id
    c = core.lower()
    return c.startswith("claude-") or c.startswith("claude_")


def is_openai_compat_model(model_id: str) -> bool:
    mid = (model_id or "").strip()
    if not mid or not openai_compat_configured():
        return False
    # Nhiều proxy (vd. chiasegpu) liệt kê cùng id Claude trong GET /v1/models lẫn Anthropic.
    # Nếu có ANTHROPIC_API_KEY thì ưu tiên Messages API cho claude-* — tránh gọi nhầm /v1 → Gemini.
    if (os.getenv("ANTHROPIC_API_KEY") or "").strip() and _is_claude_messages_style_id(mid):
        return False
    ids = list_openai_compat_model_ids()
    return mid in set(ids)
