"""Chuyển định dạng Anthropic Messages ↔ OpenAI Chat (Gemini / chiasegpu OpenAI-compat)."""
from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any


def anthropic_tools_to_openai(tools: list[dict]) -> list[dict]:
    out = []
    for t in tools:
        name = t.get("name")
        if not name:
            continue
        out.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": (t.get("description") or "")[:4096],
                    "parameters": t.get("input_schema") or {"type": "object", "properties": {}},
                },
            }
        )
    return out


def _blocks_to_openai_user_content(blocks: list) -> Any:
    """Chỉ text + image (không có tool_result)."""
    parts = []
    for block in blocks:
        if not isinstance(block, dict):
            continue
        bt = block.get("type")
        if bt == "text":
            parts.append({"type": "text", "text": block.get("text", "")})
        elif bt == "image":
            src = block.get("source") or {}
            if src.get("type") == "base64":
                mime = src.get("media_type", "image/png")
                data = src.get("data", "")
                parts.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{data}"},
                    }
                )
    if not parts:
        return ""
    if len(parts) == 1 and parts[0].get("type") == "text":
        return parts[0].get("text", "")
    return parts


def anthropic_messages_to_openai(messages: list[dict], system_text: str) -> list[dict]:
    """
    Chuyển lịch sử kiểu Anthropic (tool_use / tool_result trong content list)
    sang messages OpenAI chat.completions.
    """
    out: list[dict] = []
    if system_text and str(system_text).strip():
        out.append({"role": "system", "content": system_text})

    for m in messages:
        role = m.get("role")
        content = m.get("content")

        if role == "user":
            if isinstance(content, list):
                tool_results = [b for b in content if isinstance(b, dict) and b.get("type") == "tool_result"]
                other = [b for b in content if isinstance(b, dict) and b.get("type") != "tool_result"]
                for tr in tool_results:
                    tid = tr.get("tool_use_id") or tr.get("id") or ""
                    body = tr.get("content", tr.get("result", ""))
                    if isinstance(body, list):
                        # Anthropic content list — flatten text blocks
                        text_parts_tr = [
                            b.get("text", "") for b in body
                            if isinstance(b, dict) and b.get("type") == "text"
                        ]
                        body = "\n".join(text_parts_tr) if text_parts_tr else json.dumps(body, ensure_ascii=False)
                    elif not isinstance(body, str):
                        body = json.dumps(body, ensure_ascii=False) if body is not None else ""
                    out.append({"role": "tool", "tool_call_id": tid, "content": body})
                if other:
                    oa = _blocks_to_openai_user_content(other)
                    if oa != "" and oa is not None:
                        out.append({"role": "user", "content": oa})
                continue
            out.append({"role": "user", "content": content if isinstance(content, str) else ("" if content is None else str(content))})

        elif role == "assistant":
            if isinstance(content, str):
                out.append({"role": "assistant", "content": content})
                continue
            if isinstance(content, list):
                text_parts: list[str] = []
                tool_calls: list[dict] = []
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                    elif block.get("type") == "tool_use":
                        tid = block.get("id", "")
                        name = block.get("name", "")
                        inp = block.get("input", {})
                        try:
                            args = json.dumps(inp, ensure_ascii=False) if isinstance(inp, dict) else str(inp)
                        except Exception:
                            args = "{}"
                        tool_calls.append(
                            {
                                "id": tid,
                                "type": "function",
                                "function": {"name": name, "arguments": args},
                            }
                        )
                msg: dict[str, Any] = {"role": "assistant"}
                txt = "\n".join(text_parts).strip()
                msg["content"] = txt if txt else ""
                if tool_calls:
                    msg["tool_calls"] = tool_calls
                out.append(msg)
                continue
            out.append({"role": "assistant", "content": str(content)})

    return out


def flatten_cached_system(cached_system: str | list) -> str:
    if isinstance(cached_system, str):
        return cached_system
    if isinstance(cached_system, list):
        texts = []
        for b in cached_system:
            if isinstance(b, dict) and b.get("type") == "text":
                texts.append(b.get("text", ""))
        return "\n\n".join(texts)
    return str(cached_system or "")


def build_openai_response_like_anthropic(
    finish_reason: str | None,
    text_accumulated: str,
    tool_call_parts: dict[int, dict[str, Any]],
) -> Any:
    """Tạo object giống Anthropic message: .stop_reason, .content (text + tool_use), .usage (optional)."""
    fr = finish_reason or "stop"
    has_tools = bool(tool_call_parts)

    content_list: list[Any] = []
    if text_accumulated:
        tb = SimpleNamespace(type="text")
        tb.text = text_accumulated
        content_list.append(tb)

    for idx in sorted(tool_call_parts.keys()):
        p = tool_call_parts[idx]
        tid = p.get("id") or f"call_{idx}"
        name = p.get("name") or ""
        raw = p.get("arguments") or "{}"
        try:
            inp = json.loads(raw) if isinstance(raw, str) else raw
        except json.JSONDecodeError:
            inp = {}
        if not isinstance(inp, dict):
            inp = {}
        tub = SimpleNamespace(type="tool_use")
        tub.id = tid
        tub.name = name
        tub.input = inp
        content_list.append(tub)

    if has_tools:
        stop_reason = "tool_use"
    elif fr == "length":
        stop_reason = "max_tokens"
    else:
        stop_reason = "end_turn"

    resp = SimpleNamespace()
    resp.stop_reason = stop_reason
    resp.content = content_list
    resp.usage = None
    return resp


def usage_from_openai(usage: Any) -> Any:
    """Chuyển usage OpenAI chat.completions → object giống Anthropic (cho TokenUsageTracker)."""
    if not usage:
        return None
    return SimpleNamespace(
        input_tokens=getattr(usage, "prompt_tokens", None) or getattr(usage, "input_tokens", 0) or 0,
        output_tokens=getattr(usage, "completion_tokens", None) or getattr(usage, "output_tokens", 0) or 0,
        cache_read_input_tokens=0,
        cache_creation_input_tokens=0,
    )
