"""
Page Intent Classifier — heuristics nhanh + vision (sync) trước khi tương tác browser.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from tools.vision_dom import VisionDOM, parse_json_loose
from utils.anthropic_content import text_from_anthropic_content

# ── Intent enum ─────────────────────────────────────────────────────────────


class PageIntent(Enum):
    READY = "ready"
    LOADING = "loading"
    LOGIN_WALL = "login_wall"
    CAPTCHA = "captcha"
    RATE_LIMITED = "rate_limited"
    ERROR_PAGE = "error_page"
    MODAL_OPEN = "modal_open"
    FORM_PENDING = "form_pending"
    AUTH_EXPIRED = "auth_expired"
    BLOCKED = "blocked"
    SUCCESS = "success"
    UNKNOWN = "unknown"


# (pattern_type, patterns, intent, confidence)
HEURISTIC_RULES = [
    ("url", [r"login", r"signin", r"auth", r"account/login", r"/oauth"], PageIntent.LOGIN_WALL, 0.9),
    ("url", [r"captcha", r"challenge", r"verify", r"cf-browser-verification"], PageIntent.CAPTCHA, 0.9),
    ("url", [r"/error", r"404", r"500", r"maintenance", r"unavailable", r"not-found"], PageIntent.ERROR_PAGE, 0.85),
    ("url", [r"rate.?limit", r"too.?many"], PageIntent.RATE_LIMITED, 0.88),
    ("title", [r"rate limit", r"too many request", r"slow down", r"quá nhiều"], PageIntent.RATE_LIMITED, 0.9),
    ("title", [r"sign in", r"log in", r"đăng nhập", r"anmelden"], PageIntent.LOGIN_WALL, 0.85),
    ("title", [r"session expired", r"phiên hết hạn", r"auth expired", r"re-?login"], PageIntent.AUTH_EXPIRED, 0.88),
    ("title", [r"\b404\b", r"not found", r"forbidden", r"access denied", r"lỗi 50", r"maintenance"], PageIntent.ERROR_PAGE, 0.8),
    ("title", [r"captcha", r"verify you are human", r"xác minh"], PageIntent.CAPTCHA, 0.85),
]


def fast_classify(page) -> Tuple[PageIntent, float]:
    """URL + title + DOM nhẹ + readyState — không gọi API."""
    try:
        from tools.browser import _detect_block_or_captcha

        blocked, reason = _detect_block_or_captcha(page)
        if blocked:
            rl = (reason or "").lower()
            if any(x in rl for x in ("captcha", "hcaptcha", "recaptcha", "verify", "robot", "human")):
                return PageIntent.CAPTCHA, 0.95
            if "cloudflare" in rl or "attention" in rl or "chặn" in rl:
                return PageIntent.BLOCKED, 0.9
            return PageIntent.CAPTCHA, 0.85
    except Exception:
        pass

    try:
        url = (page.url or "").lower()
    except Exception:
        url = ""
    try:
        title = (page.title() or "").lower()
    except Exception:
        title = ""

    for pattern_type, patterns, intent, conf in HEURISTIC_RULES:
        source = url if pattern_type == "url" else title
        for p in patterns:
            if re.search(p, source, re.I):
                return intent, conf

    try:
        ready_state = page.evaluate("() => document.readyState")
    except Exception:
        ready_state = "complete"
    if ready_state != "complete":
        return PageIntent.LOADING, 0.95

    try:
        has_modal = page.evaluate(
            """() => !!document.querySelector(
            '[role="dialog"],[role="alertdialog"],.modal.show,.modal-open,[data-modal-open="true"]'
        )"""
        )
    except Exception:
        has_modal = False
    if has_modal:
        return PageIntent.MODAL_OPEN, 0.85

    try:
        busy = page.evaluate(
            """() => !!document.querySelector(
            'button[type="submit"][aria-busy="true"], .loading:not(:empty), [data-loading="true"]'
        )"""
        )
    except Exception:
        busy = False
    if busy:
        return PageIntent.FORM_PENDING, 0.7

    return PageIntent.READY, 0.75


VISION_PROMPT = """Nhìn screenshot viewport này, trang web đang ở trạng thái nào?
Chỉ trả về JSON thuần (không markdown):
{
  "intent": "ready|loading|login_wall|captcha|rate_limited|error_page|modal_open|form_pending|auth_expired|blocked|success|unknown",
  "confidence": 0.95,
  "reason": "lý do ngắn gọn tiếng Việt",
  "suggested_action": "proceed|wait|login|notify_user|retry_later|handle_modal"
}"""


def _intent_from_string(s: str) -> PageIntent:
    s = (s or "unknown").strip().lower()
    for p in PageIntent:
        if p.value == s:
            return p
    aliases = {
        "signin": PageIntent.LOGIN_WALL,
        "sign_in": PageIntent.LOGIN_WALL,
    }
    return aliases.get(s, PageIntent.UNKNOWN)


def vision_classify(page, anthropic_client, model: str) -> Tuple[PageIntent, float, str, str]:
    """Screenshot + vision model khi heuristic không đủ."""
    _, b64 = VisionDOM.capture_screenshot(page)
    response = anthropic_client.messages.create(
        model=model,
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": b64,
                        },
                    },
                    {"type": "text", "text": VISION_PROMPT},
                ],
            }
        ],
    )
    raw = text_from_anthropic_content(response.content)
    try:
        data = parse_json_loose(raw)
    except Exception:
        return PageIntent.UNKNOWN, 0.0, "vision_parse_error", "proceed"

    intent = _intent_from_string(str(data.get("intent", "unknown")))
    conf = float(data.get("confidence", 0.5))
    reason = str(data.get("reason", ""))
    sug = str(data.get("suggested_action", "proceed"))
    return intent, conf, reason, sug


ACTION_MAP = {
    PageIntent.READY: "proceed",
    PageIntent.LOADING: "wait",
    PageIntent.LOGIN_WALL: "login",
    PageIntent.CAPTCHA: "notify_user",
    PageIntent.RATE_LIMITED: "retry_later",
    PageIntent.ERROR_PAGE: "notify_user",
    PageIntent.MODAL_OPEN: "handle_modal",
    PageIntent.FORM_PENDING: "wait",
    PageIntent.AUTH_EXPIRED: "login",
    PageIntent.BLOCKED: "notify_user",
    PageIntent.SUCCESS: "proceed",
    PageIntent.UNKNOWN: "proceed",
}


@dataclass
class ClassificationResult:
    intent: PageIntent
    confidence: float
    reason: str
    suggested_action: str
    used_vision: bool


def classify_page_sync(
    page,
    anthropic_client,
    model: str,
    use_vision_threshold: float = 0.7,
) -> ClassificationResult:
    intent, conf = fast_classify(page)
    used_vision = False
    reason = f"heuristic:{intent.value}"
    suggested = ACTION_MAP.get(intent, "proceed")

    if conf < use_vision_threshold and anthropic_client is not None:
        try:
            v_intent, v_conf, v_reason, v_sug = vision_classify(page, anthropic_client, model)
            used_vision = True
            intent, conf = v_intent, v_conf
            reason = v_reason or f"vision:{v_intent.value}"
            suggested = v_sug if v_sug else ACTION_MAP.get(intent, "proceed")
        except Exception as ex:
            reason = f"vision_failed:{ex}"

    if not used_vision:
        suggested = ACTION_MAP.get(intent, "proceed")

    return ClassificationResult(
        intent=intent,
        confidence=conf,
        reason=reason,
        suggested_action=suggested,
        used_vision=used_vision,
    )


def format_intent_block_message(cr: ClassificationResult, page_url: str = "") -> str:
    """Thông báo lỗi chuẩn khi chặn action."""
    u = page_url or ""
    if cr.intent == PageIntent.CAPTCHA:
        return (
            "Error: [page_intent:captcha] Trang yêu cầu xác thực bot/CAPTCHA — "
            "cần xử lý thủ công. Không tự bypass."
        )
    if cr.intent == PageIntent.LOGIN_WALL:
        return f"Error: [page_intent:login_wall] Cần đăng nhập để tiếp tục. URL: {u}"
    if cr.intent == PageIntent.AUTH_EXPIRED:
        return "Error: [page_intent:auth_expired] Phiên đăng nhập có vẻ hết hạn — đăng nhập lại."
    if cr.intent == PageIntent.BLOCKED:
        return "Error: [page_intent:blocked] Truy cập bị chặn (IP/tài khoản/CDN)."
    if cr.intent == PageIntent.RATE_LIMITED:
        return "Error: [page_intent:rate_limited] Bị giới hạn tốc độ — thử lại sau."
    if cr.intent == PageIntent.ERROR_PAGE:
        return "Error: [page_intent:error_page] Trang lỗi (404/500/bảo trì)."
    return ""


def should_block_action(cr: ClassificationResult, page_url: str = "") -> Optional[str]:
    """Trả về chuỗi lỗi nếu phải chặn; None nếu được phép tiếp tục."""
    if cr.intent in (
        PageIntent.CAPTCHA,
        PageIntent.LOGIN_WALL,
        PageIntent.AUTH_EXPIRED,
        PageIntent.BLOCKED,
        PageIntent.RATE_LIMITED,
        PageIntent.ERROR_PAGE,
    ):
        return format_intent_block_message(cr, page_url)
    return None
