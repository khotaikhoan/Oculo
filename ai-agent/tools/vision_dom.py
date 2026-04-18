"""
Visual DOM understanding — vision-based coordinates for browser automation.
Đồng bộ (sync) với Playwright sync_api và Anthropic client trong server.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import random
import re
import sys
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw

from tools.human_behavior import HumanMouse, HumanTiming
from utils.anthropic_content import text_from_anthropic_content

# ── Data models ─────────────────────────────────────────────────────────────


@dataclass
class VisualElement:
    label: str
    x: int
    y: int
    width: int
    height: int
    confidence: float
    element_type: str
    suggested_action: str
    bbox: Tuple[int, int, int, int]


@dataclass
class PageAnalysis:
    page_type: str
    page_intent: str
    elements: List[VisualElement]
    scroll_needed: bool
    has_modal: bool
    has_captcha: bool
    screenshot_base64: str
    viewport_width: int
    viewport_height: int
    full_page_height: int


def _extract_json_text(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        if len(parts) >= 2:
            chunk = parts[1]
            if chunk.lstrip().startswith("json"):
                chunk = chunk.lstrip()[4:].lstrip()
            raw = chunk
    return raw.strip()


def parse_json_loose(raw: str) -> Dict[str, Any]:
    raw = _extract_json_text(raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            return json.loads(m.group(0))
        raise


# ── Cache ────────────────────────────────────────────────────────────────────


class VisionCache:
    """Cache PageAnalysis theo URL + hash screenshot (TTL ngắn)."""

    def __init__(self, ttl_seconds: int = 30):
        self._cache: Dict[str, dict] = {}
        self.ttl = ttl_seconds

    def _key(self, url: str, screenshot_bytes: bytes) -> str:
        h = hashlib.md5()
        h.update(url.encode("utf-8"))
        h.update(screenshot_bytes[: min(len(screenshot_bytes), 8192)])
        return h.hexdigest()

    def get(self, url: str, screenshot_bytes: bytes) -> Optional[PageAnalysis]:
        key = self._key(url, screenshot_bytes)
        entry = self._cache.get(key)
        if entry and time.time() - entry["ts"] < self.ttl:
            return entry["data"]
        return None

    def set(self, url: str, screenshot_bytes: bytes, analysis: PageAnalysis) -> None:
        key = self._key(url, screenshot_bytes)
        self._cache[key] = {"data": analysis, "ts": time.time(), "url": url}

    def invalidate_url(self, url: str) -> None:
        to_del = [k for k, v in self._cache.items() if v.get("url") == url]
        for k in to_del:
            del self._cache[k]


vision_cache = VisionCache(ttl_seconds=int(os.getenv("VISION_CACHE_TTL", "30")))


# ── VisionDOM ────────────────────────────────────────────────────────────────


class VisionDOM:
    """Vision-based layout analysis (sync)."""

    ANALYSIS_SYSTEM_PROMPT = """Bạn là computer vision expert phân tích giao diện web.

Nhiệm vụ: nhìn vào screenshot và trả về JSON mô tả chính xác vị trí các element tương tác.

QUY TẮC QUAN TRỌNG:
- Tọa độ (x, y) là CENTER của element, tính bằng pixel tuyệt đối
- x tính từ trái sang phải (0 = trái màn hình)
- y tính từ trên xuống dưới (0 = đầu trang)
- Viewport thường ~1440 × 900 (có thể khác — dùng đúng kích thước ảnh)
- Chỉ liệt kê element VISIBLE và INTERACTIVE
- Confidence: 1.0 = chắc chắn, 0.7 = khá chắc, < 0.5 = không chắc

ELEMENT TYPES: button | input | link | select | checkbox | textarea | image | text

RESPONSE FORMAT — chỉ trả về JSON thuần, không markdown:
{
  "page_type": "login|dashboard|form|listing|article|unknown",
  "page_intent": "mô tả ngắn gọn trang đang làm gì",
  "has_modal": false,
  "has_captcha": false,
  "scroll_needed": false,
  "elements": [
    {
      "label": "tên mô tả element bằng tiếng Việt",
      "x": 720,
      "y": 450,
      "width": 120,
      "height": 40,
      "confidence": 0.95,
      "element_type": "button",
      "suggested_action": "click",
      "bbox": [660, 430, 780, 470]
    }
  ]
}"""

    FIND_ELEMENT_PROMPT = """Tìm element "{target}" trong screenshot.

Trả về JSON:
{{
  "found": true,
  "x": 720,
  "y": 340,
  "width": 150,
  "height": 44,
  "confidence": 0.92,
  "element_type": "button",
  "reasoning": "Thấy nút màu xanh có text 'Đăng nhập' ở góc phải header"
}}

Nếu không tìm thấy:
{{
  "found": false,
  "confidence": 0,
  "reasoning": "Không thấy element này trong viewport hiện tại",
  "suggestion": "scroll_down"
}}

suggestion phải là một trong: scroll_down | scroll_up | check_modal | not_on_page"""

    @staticmethod
    def capture_screenshot(page) -> Tuple[bytes, str]:
        screenshot_bytes = page.screenshot(type="jpeg", quality=85, full_page=False, timeout=8000)
        b64 = base64.b64encode(screenshot_bytes).decode("ascii")
        return screenshot_bytes, b64

    @staticmethod
    def annotate_grid(screenshot_bytes: bytes, grid_size: int = 100) -> str:
        img = Image.open(io.BytesIO(screenshot_bytes)).convert("RGBA")
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        w, h = img.size
        for x in range(0, w, grid_size):
            draw.line([(x, 0), (x, h)], fill=(100, 100, 255, 40), width=1)
            if x > 0:
                draw.text((x + 2, 2), str(x), fill=(100, 100, 255, 180))
        for y in range(0, h, grid_size):
            draw.line([(0, y), (w, y)], fill=(100, 100, 255, 40), width=1)
            if y > 0:
                draw.text((2, y + 2), str(y), fill=(100, 100, 255, 180))
        result = Image.alpha_composite(img, overlay).convert("RGB")
        buf = io.BytesIO()
        result.save(buf, format="JPEG", quality=80)
        return base64.b64encode(buf.getvalue()).decode("ascii")

    @classmethod
    def analyze_page(
        cls,
        page,
        anthropic_client,
        model: str,
        focus: Optional[str] = None,
        use_cache: bool = True,
    ) -> PageAnalysis:
        screenshot_bytes, b64_raw = cls.capture_screenshot(page)
        url = ""
        try:
            url = page.url or ""
        except Exception:
            pass

        if use_cache:
            cached = vision_cache.get(url, screenshot_bytes)
            if cached is not None:
                return cached

        b64_annotated = cls.annotate_grid(screenshot_bytes)
        vp = page.viewport_size or {"width": 1440, "height": 900}
        vw, vh = int(vp.get("width", 1440)), int(vp.get("height", 900))
        try:
            full_height = int(page.evaluate("() => document.body ? document.body.scrollHeight : 0") or 0)
        except Exception:
            full_height = 0

        extra = ""
        if focus:
            extra = f"\n\nTập trung tìm / mô tả thêm về: {focus}"

        user_text = (
            f"Phân tích trang web này. Viewport: {vw}×{vh}px. "
            f"Full page height: {full_height}px. URL: {url}{extra}"
        )

        response = anthropic_client.messages.create(
            model=model,
            max_tokens=2000,
            system=cls.ANALYSIS_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": b64_annotated,
                            },
                        },
                        {"type": "text", "text": user_text},
                    ],
                }
            ],
        )
        raw = text_from_anthropic_content(response.content)
        data = parse_json_loose(raw)

        elements: List[VisualElement] = []
        for e in data.get("elements") or []:
            try:
                bbox_raw = e.get("bbox")
                if bbox_raw and len(bbox_raw) == 4:
                    bbox = (int(bbox_raw[0]), int(bbox_raw[1]), int(bbox_raw[2]), int(bbox_raw[3]))
                else:
                    cx, cy = int(e["x"]), int(e["y"])
                    ww = int(e.get("width", 80))
                    hh = int(e.get("height", 32))
                    bbox = (cx - ww // 2, cy - hh // 2, cx + ww // 2, cy + hh // 2)
                elements.append(
                    VisualElement(
                        label=str(e.get("label", "")),
                        x=int(e["x"]),
                        y=int(e["y"]),
                        width=int(e.get("width", bbox[2] - bbox[0])),
                        height=int(e.get("height", bbox[3] - bbox[1])),
                        confidence=float(e.get("confidence", 0.7)),
                        element_type=str(e.get("element_type", "unknown")),
                        suggested_action=str(e.get("suggested_action", "click")),
                        bbox=bbox,
                    )
                )
            except Exception:
                continue

        analysis = PageAnalysis(
            page_type=str(data.get("page_type", "unknown")),
            page_intent=str(data.get("page_intent", "")),
            elements=elements,
            scroll_needed=bool(data.get("scroll_needed", False)),
            has_modal=bool(data.get("has_modal", False)),
            has_captcha=bool(data.get("has_captcha", False)),
            screenshot_base64=b64_raw,
            viewport_width=vw,
            viewport_height=vh,
            full_page_height=full_height,
        )
        if use_cache:
            vision_cache.set(url, screenshot_bytes, analysis)
        return analysis

    @classmethod
    def find_element(
        cls,
        page,
        target: str,
        anthropic_client,
        model: str,
        scroll_attempts: int = 3,
    ) -> Optional[VisualElement]:
        prompt = cls.FIND_ELEMENT_PROMPT.format(target=target)

        for _ in range(scroll_attempts):
            screenshot_bytes, _ = cls.capture_screenshot(page)
            b64 = cls.annotate_grid(screenshot_bytes)

            response = anthropic_client.messages.create(
                model=model,
                max_tokens=600,
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
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            )
            raw = text_from_anthropic_content(response.content)
            try:
                data = parse_json_loose(raw)
            except Exception:
                time.sleep(0.5)
                continue

            if data.get("found") and float(data.get("confidence", 0)) >= 0.65:
                w = int(data.get("width", 100))
                h = int(data.get("height", 40))
                x, y = int(data["x"]), int(data["y"])
                bbox_raw = data.get("bbox")
                if bbox_raw and len(bbox_raw) == 4:
                    bbox = (int(bbox_raw[0]), int(bbox_raw[1]), int(bbox_raw[2]), int(bbox_raw[3]))
                else:
                    bbox = (x - w // 2, y - h // 2, x + w // 2, y + h // 2)
                return VisualElement(
                    label=target,
                    x=x,
                    y=y,
                    width=w,
                    height=h,
                    confidence=float(data["confidence"]),
                    element_type=str(data.get("element_type", "unknown")),
                    suggested_action="click",
                    bbox=bbox,
                )

            suggestion = str(data.get("suggestion", "scroll_down"))
            if suggestion == "not_on_page":
                return None
            if suggestion == "scroll_up":
                page.mouse.wheel(0, -400)
            elif suggestion == "check_modal":
                pass
            else:
                page.mouse.wheel(0, 400)
            time.sleep(0.8)

        return None


# ── VisionExecutor ───────────────────────────────────────────────────────────


class VisionExecutor:
    """Thực thi click/type dựa trên vision + HumanMouse (sync)."""

    CONFIDENCE_CLICK_MIN = 0.75

    @staticmethod
    def verify_action(page, anthropic_client, model: str, expected_change: str) -> Dict[str, Any]:
        _, b64 = VisionDOM.capture_screenshot(page)
        response = anthropic_client.messages.create(
            model=model,
            max_tokens=400,
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
                        {
                            "type": "text",
                            "text": (
                                f"Context: {expected_change}\n\n"
                                "Trang web hiện tại đang hiển thị gì? "
                                "Action có vẻ thành công không? "
                                'Trả về JSON: {"success": true/false, "current_state": "mô tả", '
                                '"next_suggested_action": "gợi ý bước tiếp"}'
                            ),
                        },
                    ],
                }
            ],
        )
        raw = text_from_anthropic_content(response.content)
        try:
            return parse_json_loose(raw)
        except Exception:
            return {"success": None, "raw": raw[:500]}

    @classmethod
    def vision_click(
        cls,
        page,
        target: str,
        anthropic_client,
        model: str,
        verify: bool = True,
    ) -> Dict[str, Any]:
        element = VisionDOM.find_element(page, target, anthropic_client, model)
        if not element:
            return {
                "success": False,
                "error": f"Không tìm thấy element: '{target}'",
                "suggestion": "Thử mô tả khác hoặc scroll trang",
            }

        if element.confidence < cls.CONFIDENCE_CLICK_MIN:
            return {
                "success": False,
                "low_confidence": True,
                "confidence": element.confidence,
                "found_at": [element.x, element.y],
                "reasoning": (
                    f"Tìm thấy nhưng không chắc (confidence: {element.confidence:.0%}). "
                    "Cần mô tả rõ hơn hoặc dùng browser_evaluate."
                ),
            }

        HumanTiming.think(100, 300)
        HumanMouse.click(page, element.x, element.y)
        HumanTiming.after_click()

        try:
            vision_cache.invalidate_url(page.url or "")
        except Exception:
            pass

        result: Dict[str, Any] = {
            "success": True,
            "clicked_element": element.label,
            "coordinates": [element.x, element.y],
            "confidence": element.confidence,
            "element_type": element.element_type,
        }

        if verify:
            time.sleep(0.8)
            result["verification"] = cls.verify_action(
                page, anthropic_client, model, f"Sau khi click '{target}'"
            )
        return result

    @classmethod
    def vision_type(
        cls,
        page,
        target: str,
        text: str,
        anthropic_client,
        model: str,
    ) -> Dict[str, Any]:
        element = VisionDOM.find_element(page, target, anthropic_client, model)
        if not element:
            return {"success": False, "error": f"Không tìm thấy input: '{target}'"}

        HumanMouse.click(page, element.x, element.y)
        HumanTiming.think(100, 250)

        try:
            page.keyboard.press("ControlOrMeta+A")
        except Exception:
            mod = "Meta+A" if sys.platform == "darwin" else "Control+A"
            try:
                page.keyboard.press(mod)
            except Exception:
                pass
        time.sleep(0.1)
        page.keyboard.press("Backspace")
        time.sleep(0.1)

        for char in text:
            page.keyboard.type(char, delay=0)
            time.sleep(HumanTiming.typing_delay(char))

        try:
            vision_cache.invalidate_url(page.url or "")
        except Exception:
            pass

        return {
            "success": True,
            "typed_into": element.label,
            "text_length": len(text),
            "coordinates": [element.x, element.y],
        }


# ── HybridBrowserExecutor ────────────────────────────────────────────────────


class HybridBrowserExecutor:
    """Selector / text locator trước, vision sau (sync)."""

    @classmethod
    def smart_click(
        cls,
        page,
        target: Optional[str],
        selector: Optional[str],
        anthropic_client,
        model: str,
        verify: bool = True,
    ) -> Dict[str, Any]:
        sel = (selector or "").strip()
        txt = (target or "").strip()

        if sel:
            try:
                loc = page.locator(sel).first
                loc.wait_for(state="visible", timeout=3000)
                box = loc.bounding_box()
                if box:
                    cx = int(box["x"] + box["width"] * random.uniform(0.3, 0.7))
                    cy = int(box["y"] + box["height"] * random.uniform(0.3, 0.7))
                    HumanTiming.think(200, 500)
                    HumanMouse.click(page, cx, cy)
                    HumanTiming.after_click()
                    return {"success": True, "method": "selector", "selector": sel}
            except Exception:
                pass

        if txt:
            try:
                loc = page.get_by_text(txt, exact=False)
                if loc.count() > 0:
                    el = loc.first
                    el.scroll_into_view_if_needed(timeout=5000)
                    box = el.bounding_box()
                    if box:
                        cx = int(box["x"] + box["width"] * random.uniform(0.3, 0.7))
                        cy = int(box["y"] + box["height"] * random.uniform(0.3, 0.7))
                        HumanTiming.think(200, 500)
                        HumanMouse.click(page, cx, cy)
                        HumanTiming.after_click()
                        return {"success": True, "method": "text_locator", "text": txt}
            except Exception:
                pass

        if anthropic_client and txt:
            return VisionExecutor.vision_click(page, txt, anthropic_client, model, verify=verify)

        return {
            "success": False,
            "error": "Tất cả strategy đều fail",
            "tried": ["selector", "text_locator", "vision"],
        }


# ── Tool entrypoints (trả về str cho run_tool) ────────────────────────────────


def _get_page_safe():
    from tools import browser

    return browser._get_page()


def browser_analyze_page_tool(anthropic_client, model: str, focus: Optional[str]) -> str:
    from tools.browser import BrowserCDPError

    try:
        page = _get_page_safe()
    except BrowserCDPError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"
    try:
        analysis = VisionDOM.analyze_page(page, anthropic_client, model, focus=focus)
        payload = asdict(analysis)
        for el in payload["elements"]:
            if isinstance(el.get("bbox"), tuple):
                el["bbox"] = list(el["bbox"])
        return json.dumps(payload, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: browser_analyze_page failed: {e}"


def browser_vision_click_tool(
    anthropic_client,
    model: str,
    target: str,
    verify: bool,
    selector: Optional[str],
) -> str:
    from tools.browser import BrowserCDPError

    if not (target or "").strip() and not (selector or "").strip():
        return "Error: Cần `target` (mô tả) hoặc `selector`."

    try:
        page = _get_page_safe()
    except BrowserCDPError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"

    try:
        result = HybridBrowserExecutor.smart_click(
            page,
            target.strip() if target else None,
            (selector or "").strip() or None,
            anthropic_client,
            model,
            verify=verify,
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: browser_vision_click failed: {e}"


def browser_vision_type_tool(anthropic_client, model: str, target: str, text: str) -> str:
    from tools.browser import BrowserCDPError

    if not target or not text:
        return "Error: `target` và `text` là bắt buộc."
    try:
        page = _get_page_safe()
    except BrowserCDPError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"
    try:
        result = VisionExecutor.vision_type(page, target, text, anthropic_client, model)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: browser_vision_type failed: {e}"
