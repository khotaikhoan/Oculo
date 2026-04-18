"""Unit / E2E nhẹ cho page_classifier (sync Playwright)."""
from __future__ import annotations

import os
import tempfile

import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import Error as PlaywrightError

from tools.browser import ANTI_DETECTION_INIT, DEFAULT_USER_AGENT, _viewport
from tools.page_classifier import (
    PageIntent,
    classify_page_sync,
    fast_classify,
    should_block_action,
)


def _iso_page(pw, headless: bool | None = None):
    if headless is None:
        headless = os.getenv("BROWSER_HEADLESS", "1").lower() in ("1", "true", "yes")
    tmp = tempfile.mkdtemp(prefix="oculo_pc_")
    vp = _viewport()
    kwargs = dict(
        user_data_dir=tmp,
        headless=headless,
        viewport=vp,
        user_agent=DEFAULT_USER_AGENT,
    )
    ctx = pw.chromium.launch_persistent_context(**kwargs)
    ctx.add_init_script(ANTI_DETECTION_INIT)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.set_viewport_size(vp)
    return ctx, page


@pytest.fixture
def pc_page():
    with sync_playwright() as pw:
        try:
            ctx, page = _iso_page(pw)
        except PlaywrightError as e:
            # CI / local dev may not have Playwright browsers installed.
            if "playwright install" in str(e) or "Executable doesn't exist" in str(e):
                pytest.skip("Playwright browsers not installed (run `playwright install`).")
            raise
        try:
            yield page
        finally:
            ctx.close()


@pytest.mark.e2e
def test_fast_login_title(pc_page):
    pc_page.set_content(
        "<!DOCTYPE html><html><head><title>Sign in to continue</title></head><body>x</body></html>"
    )
    intent, conf = fast_classify(pc_page)
    assert intent == PageIntent.LOGIN_WALL
    assert conf >= 0.8


@pytest.mark.e2e
def test_fast_ready_simple(pc_page):
    pc_page.set_content(
        "<!DOCTYPE html><html><head><title>Hello</title></head>"
        "<body><p>Hi</p></body></html>"
    )
    intent, conf = fast_classify(pc_page)
    assert intent == PageIntent.READY
    assert conf >= 0.7


@pytest.mark.e2e
def test_fast_modal_open(pc_page):
    pc_page.set_content(
        '<!DOCTYPE html><html><body><div role="dialog">Modal</div></body></html>'
    )
    intent, conf = fast_classify(pc_page)
    assert intent == PageIntent.MODAL_OPEN
    assert conf >= 0.8


@pytest.mark.e2e
def test_captcha_blocks(pc_page):
    pc_page.set_content(
        "<html><head><title>ok</title></head><body>recaptcha verify you are human</body></html>"
    )
    cr = classify_page_sync(pc_page, None, "claude-sonnet-4-5", use_vision_threshold=1.0)
    assert cr.intent == PageIntent.CAPTCHA
    msg = should_block_action(cr, pc_page.url or "")
    assert msg and "captcha" in msg.lower()


@pytest.mark.e2e
def test_vision_fallback_when_heuristic_unknown(monkeypatch, pc_page):
    """Heuristic trả confidence thấp → gọi vision (mock)."""
    pc_page.set_content("<html><body><div>Test</div></body></html>")

    def fake_fast(_page):
        return PageIntent.UNKNOWN, 0.0

    monkeypatch.setattr("tools.page_classifier.fast_classify", fake_fast)

    class FakeContent:
        type = "text"
        text = '{"intent":"ready","confidence":0.9,"reason":"ok","suggested_action":"proceed"}'

    class FakeResp:
        content = [FakeContent()]

    class FakeClient:
        class Messages:
            def create(self, **kwargs):
                return FakeResp()

        messages = Messages()

    cr = classify_page_sync(pc_page, FakeClient(), "m", use_vision_threshold=0.7)
    assert cr.used_vision is True
    assert cr.intent == PageIntent.READY
