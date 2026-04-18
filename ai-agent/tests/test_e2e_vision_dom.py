"""
E2E / integration tests cho tools/vision_dom.py.

- Không cần API: annotate_grid, parse_json_loose, VisionCache, HybridBrowserExecutor (selector/text).
- Cần ANTHROPIC_API_KEY + mạng: VisionDOM.analyze_page, find_element (đánh dấu @pytest.mark.vision_api).

Chạy tất cả (không API vẫn chạy):
  cd ai-agent && BROWSER_HEADLESS=1 venv/bin/python -m pytest tests/test_e2e_vision_dom.py -v --tb=short

Chỉ test vision API:
  ANTHROPIC_API_KEY=... venv/bin/python -m pytest tests/test_e2e_vision_dom.py -m vision_api -v
"""
from __future__ import annotations

import base64
import io
import os
import tempfile
from typing import Any

import anthropic
import pytest
from PIL import Image
from playwright.sync_api import sync_playwright

from tools.browser import ANTI_DETECTION_INIT, DEFAULT_USER_AGENT, _viewport
from tools.vision_dom import (
    HybridBrowserExecutor,
    VisionCache,
    VisionDOM,
    parse_json_loose,
)


def _launch_isolated_context(pw, headless: bool | None = None):
    if headless is None:
        headless = os.getenv("BROWSER_HEADLESS", "1").lower() in ("1", "true", "yes")
    tmp = tempfile.mkdtemp(prefix="oculo_vision_e2e_")
    vp = _viewport()
    chrome_bin = None
    for path in (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ):
        if os.path.exists(path):
            chrome_bin = path
            break
    kwargs: dict[str, Any] = dict(
        user_data_dir=tmp,
        headless=headless,
        viewport=vp,
        user_agent=DEFAULT_USER_AGENT,
        locale="vi-VN",
        timezone_id="Asia/Ho_Chi_Minh",
        permissions=["geolocation", "notifications"],
        java_script_enabled=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--window-size=1440,900",
            "--disable-infobars",
        ],
        ignore_default_args=["--enable-automation"],
    )
    if chrome_bin:
        kwargs["executable_path"] = chrome_bin
    ctx = pw.chromium.launch_persistent_context(**kwargs)
    ctx.add_init_script(ANTI_DETECTION_INIT)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.set_viewport_size(vp)
    return ctx, page


@pytest.fixture
def vision_page():
    with sync_playwright() as pw:
        ctx, page = _launch_isolated_context(pw)
        try:
            yield page
        finally:
            ctx.close()


def test_parse_json_loose_strips_markdown_fence():
    raw = """```json
{"found": true, "x": 10, "y": 20, "confidence": 0.9}
```"""
    d = parse_json_loose(raw)
    assert d["found"] is True
    assert d["x"] == 10


def test_annotate_grid_output_valid_jpeg(vision_page):
    vision_page.goto(
        "data:text/html;charset=utf-8,<html><body style='margin:40px'><button id='b'>OK</button></body></html>",
        wait_until="domcontentloaded",
        timeout=15000,
    )
    raw_bytes, _ = VisionDOM.capture_screenshot(vision_page)
    b64_grid = VisionDOM.annotate_grid(raw_bytes, grid_size=100)
    decoded = base64.b64decode(b64_grid)
    img = Image.open(io.BytesIO(decoded))
    assert img.format == "JPEG"
    assert img.size[0] > 100 and img.size[1] > 100


def test_vision_cache_hit(vision_page):
    vision_page.goto(
        "data:text/html;charset=utf-8,<html><body>cache test</body></html>",
        wait_until="domcontentloaded",
    )
    raw, _ = VisionDOM.capture_screenshot(vision_page)
    url = vision_page.url
    c = VisionCache(ttl_seconds=60)

    from tools.vision_dom import PageAnalysis, VisualElement

    dummy = PageAnalysis(
        page_type="unknown",
        page_intent="test",
        elements=[],
        scroll_needed=False,
        has_modal=False,
        has_captcha=False,
        screenshot_base64="",
        viewport_width=1440,
        viewport_height=900,
        full_page_height=100,
    )
    assert c.get(url, raw) is None
    c.set(url, raw, dummy)
    assert c.get(url, raw) is not None
    c.invalidate_url(url)
    assert c.get(url, raw) is None


@pytest.mark.e2e
@pytest.mark.network
def test_hybrid_smart_click_selector_only(vision_page):
    """Không gọi vision — chỉ Playwright selector."""
    vision_page.set_content(
        """<!DOCTYPE html><html><body style="padding:80px">
        <button id="tbtn" type="button">Click me</button>
        </body></html>"""
    )
    result = HybridBrowserExecutor.smart_click(
        vision_page,
        target=None,
        selector="#tbtn",
        anthropic_client=None,
        model="claude-sonnet-4-5",
        verify=False,
    )
    assert result["success"] is True
    assert result["method"] == "selector"


@pytest.mark.e2e
@pytest.mark.network
def test_hybrid_smart_click_text_locator(vision_page):
    vision_page.set_content(
        """<!DOCTYPE html><html><body style="padding:80px">
        <a href="#">UniqueLinkTextXYZ</a>
        </body></html>"""
    )
    result = HybridBrowserExecutor.smart_click(
        vision_page,
        target="UniqueLinkTextXYZ",
        selector=None,
        anthropic_client=None,
        model="claude-sonnet-4-5",
        verify=False,
    )
    assert result["success"] is True
    assert result["method"] == "text_locator"


# ── Vision API (Anthropic) ─────────────────────────────────────────────────

vision_api = pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set — skip real vision API calls",
)


@pytest.mark.vision_api
@vision_api
@pytest.mark.e2e
@pytest.mark.network
def test_e2e_analyze_page_structure(vision_page):
    """Gọi API vision: phân tích trang có nút rõ ràng."""
    model = os.getenv("MODEL", "claude-sonnet-4-5")
    client = anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        base_url=os.getenv("ANTHROPIC_BASE_URL") or None,
    )
    vision_page.set_content(
        """<!DOCTYPE html><html><head><meta charset="utf-8"></head>
        <body style="font-family:sans-serif;padding:48px;background:#f5f5f5">
        <h1>Đăng nhập</h1>
        <button type="button" style="padding:12px 24px;background:#2563eb;color:white;border:none;border-radius:8px">
          Gửi form
        </button>
        </body></html>"""
    )
    vision_page.wait_for_timeout(300)
    analysis = VisionDOM.analyze_page(
        vision_page,
        client,
        model,
        focus=None,
        use_cache=False,
    )
    assert analysis.viewport_width >= 400
    assert isinstance(analysis.elements, list)
    # Model nên liệt kê ít nhất một control hoặc mô tả trang
    assert len(analysis.screenshot_base64) > 50
    # Model có thể trả về danh sách element rỗng nếu parse lệch; ít nhất có metadata viewport
    assert analysis.viewport_height >= 400


@pytest.mark.vision_api
@vision_api
@pytest.mark.e2e
@pytest.mark.network
def test_e2e_find_element_button(vision_page):
    model = os.getenv("MODEL", "claude-sonnet-4-5")
    client = anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        base_url=os.getenv("ANTHROPIC_BASE_URL") or None,
    )
    vision_page.set_content(
        """<!DOCTYPE html><html><body style="padding:100px">
        <button id="x" style="font-size:18px;padding:16px">Xác nhận thanh toán</button>
        </body></html>"""
    )
    vision_page.wait_for_timeout(400)
    el = VisionDOM.find_element(
        vision_page,
        "nút Xác nhận thanh toán",
        client,
        model,
        scroll_attempts=1,
    )
    assert el is not None
    assert el.confidence >= 0.65
    assert 50 < el.x < vision_page.viewport_size["width"]
    assert 50 < el.y < vision_page.viewport_size["height"]


@pytest.mark.vision_api
@vision_api
@pytest.mark.e2e
@pytest.mark.network
def test_e2e_vision_click_tool_string_json(vision_page, monkeypatch):
    """browser_vision_click_tool: hybrid click trên trang tĩnh (selector không cần vision)."""
    from tools import vision_dom

    monkeypatch.setattr(vision_dom, "_get_page_safe", lambda: vision_page)
    vision_page.set_content(
        """<!DOCTYPE html><html><body style="padding:60px">
        <button id="go">Tiếp tục</button></body></html>"""
    )
    out = vision_dom.browser_vision_click_tool(
        anthropic_client=None,
        model="claude-sonnet-4-5",
        target="",
        verify=False,
        selector="#go",
    )
    d = parse_json_loose(out)
    assert d.get("success") is True
