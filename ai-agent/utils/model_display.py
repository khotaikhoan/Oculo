"""Nhãn hiển thị model / backend cho UI (Anthropic Messages API)."""
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

# Prefix trong id model (nếu nhà cung cấp dùng dạng prefix/model).
# Có thể ghi đè bằng ROUTER_LABEL_<PREFIX> trong .env (prefix viết hoa, - → _).
KNOWN_MODEL_PREFIX_LABELS: dict[str, str] = {
    "csg": "chiasegpu",
    "csgm": "chiasegpu · Gemini",
    "anthropic": "Anthropic",
    "openai": "OpenAI",
    "openrouter": "OpenRouter",
    "pplx": "Perplexity",
    "perplexity": "Perplexity",
    "groq": "Groq",
    "xai": "xAI (Grok)",
    "grok": "xAI (Grok)",
    "gemini": "Google Gemini",
    "google": "Google Gemini",
    "vertex": "Google Vertex",
    "glm": "GLM (Zhipu)",
    "glm-cn": "GLM (China)",
    "deepseek": "DeepSeek",
    "mistral": "Mistral",
    "cohere": "Cohere",
    "nvidia": "NVIDIA NIM",
    "together": "Together AI",
    "fireworks": "Fireworks",
    "nebius": "Nebius",
    "siliconflow": "SiliconFlow",
    "minimax": "MiniMax",
    "kimi": "Kimi",
    "ollama": "Ollama",
}


def _label_for_prefix(router_prefix: str) -> str:
    if not router_prefix:
        return ""
    env_key = f"ROUTER_LABEL_{router_prefix.upper().replace('-', '_')}"
    env_lbl = os.getenv(env_key)
    if env_lbl:
        return env_lbl.strip()
    low = router_prefix.lower()
    return KNOWN_MODEL_PREFIX_LABELS.get(low) or KNOWN_MODEL_PREFIX_LABELS.get(
        low.split("-")[0], ""
    ) or router_prefix


def model_ui_meta(model_id: str | None) -> dict:
    """
    Trả về dict dùng cho JSON/SSE:
    - display_name: tên model ngắn (sau prefix router nếu có)
    - provider_label: nhãn nhà cung cấp / backend
    - route_hint: URL Messages API (Anthropic hoặc proxy)
    - router_prefix: phần trước / nếu có
    """
    mid = (model_id or "").strip()
    if not mid:
        return {
            "display_name": "—",
            "provider_label": "—",
            "route_hint": "",
            "router_prefix": "",
        }

    router_prefix = ""
    display_core = mid

    if "/" in mid:
        router_prefix, display_core = mid.split("/", 1)

    upstream = _label_for_prefix(router_prefix) if router_prefix else ""
    au = os.getenv("ANTHROPIC_BASE_URL")
    route_hint = au or "https://api.anthropic.com"
    if router_prefix and router_prefix.lower() == "ollama":
        provider_label = "Ollama (local)"
        route_hint = (os.getenv("OLLAMA_BASE_URL") or "http://127.0.0.1:11434").rstrip("/")
    elif router_prefix:
        provider_label = f"Anthropic API · {upstream}" if upstream else f"Anthropic API ({router_prefix})"
    else:
        provider_label = "Anthropic API"

    return {
        "display_name": display_core,
        "provider_label": provider_label,
        "route_hint": route_hint,
        "router_prefix": router_prefix,
        "full_id": mid,
    }


def model_ui_meta_openai_compat(model_id: str | None) -> dict:
    """Nhãn cho model lấy từ endpoint OpenAI-compatible (vd. Gemini qua chiasegpu)."""
    m = model_ui_meta(model_id)
    base_url = (os.getenv("GEMINI_BASE_URL") or os.getenv("OPENAI_COMPAT_BASE_URL") or "").strip()
    m["provider_label"] = os.getenv("GEMINI_PROVIDER_LABEL", "Gemini / OpenAI-compat")
    if base_url:
        m["route_hint"] = base_url
    return m


def enrich_models_list(ids: list[str], openai_compat_ids: set[str] | frozenset | None = None) -> list[dict]:
    """Danh sách model cho GET /models. `openai_compat_ids`: id từ GEMINI_BASE_URL / OpenAI-compat."""
    oc = openai_compat_ids if openai_compat_ids is not None else set()
    out: list[dict] = []
    seen = set()
    for mid in ids:
        if not mid or mid in seen:
            continue
        seen.add(mid)
        meta = model_ui_meta_openai_compat(mid) if mid in oc else model_ui_meta(mid)
        out.append(
            {
                "id": mid,
                "display_name": meta["display_name"],
                "provider_label": meta["provider_label"],
                "route_hint": meta["route_hint"],
                "router_prefix": meta["router_prefix"],
            }
        )
    return out
