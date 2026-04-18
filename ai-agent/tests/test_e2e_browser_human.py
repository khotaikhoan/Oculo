"""
E2E smoke tests — cần mạng + Playwright browsers (venv: python -m playwright install chromium).

Chạy: cd ai-agent && BROWSER_HEADLESS=1 venv/bin/python3 -m pytest tests/test_e2e_browser_human.py -v --tb=short
"""
from __future__ import annotations

import os
import re
import tempfile
from typing import Any

import pytest
from playwright.sync_api import sync_playwright

from tools.browser import (
    ANTI_DETECTION_INIT,
    DEFAULT_USER_AGENT,
    _detect_block_or_captcha,
    _viewport,
)


def _launch_isolated_human_context(pw, headless: bool | None = None):
    """Persistent context giống fallback trong tools/browser.py (profile tạm)."""
    if headless is None:
        headless = os.getenv("BROWSER_HEADLESS", "1").lower() in ("1", "true", "yes")
    tmp = tempfile.mkdtemp(prefix="oculo_e2e_profile_")
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
        bypass_csp=False,
        extra_http_headers={
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": '"Chromium";v="122", "Google Chrome";v="122"',
            "sec-ch-ua-platform": '"macOS"',
        },
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-infobars",
            "--window-size=1440,900",
            "--exclude-switches=enable-automation",
            "--disable-automation",
            "--profile-directory=Default",
        ],
        ignore_default_args=["--enable-automation", "--enable-blink-features=IdleDetection"],
    )
    if chrome_bin:
        kwargs["executable_path"] = chrome_bin
    ctx = pw.chromium.launch_persistent_context(**kwargs)
    ctx.add_init_script(ANTI_DETECTION_INIT)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.set_viewport_size(vp)
    return ctx, page


@pytest.fixture
def human_page():
    with sync_playwright() as pw:
        ctx, page = _launch_isolated_human_context(pw)
        try:
            yield page
        finally:
            ctx.close()


@pytest.mark.e2e
@pytest.mark.network
def test_navigator_webdriver_undefined_after_init(human_page):
    wd = human_page.evaluate("() => navigator.webdriver")
    assert wd in (None, False)


@pytest.mark.e2e
@pytest.mark.network
def test_detect_block_captcha_data_url(human_page):
    human_page.goto(
        "data:text/html;charset=utf-8,<html><body>recaptcha verify you are human</body></html>",
        timeout=15000,
    )
    blocked, reason = _detect_block_or_captcha(human_page)
    assert blocked is True
    assert reason


@pytest.mark.e2e
@pytest.mark.network
def test_scroll_and_click_example(human_page):
    human_page.goto("https://example.com/", wait_until="domcontentloaded", timeout=30000)
    human_page.mouse.wheel(0, 400)
    human_page.locator("a").first.click(timeout=10000)
    assert "iana" in human_page.url.lower() or human_page.url.startswith("https://")


@pytest.mark.e2e
@pytest.mark.network
def test_duckduckgo_search_click_first(human_page):
    """Tương đương scenario Google search — DDG ít consent hơn."""
    q = "oculo ai agent"
    human_page.goto(
        "https://duckduckgo.com/?q=" + q.replace(" ", "+"),
        wait_until="domcontentloaded",
        timeout=45000,
    )
    human_page.wait_for_timeout(2500)
    # Kết quả organic: liên kết có data-testid hoặc .result__a
    link = human_page.locator("a[data-testid='result-title-a'], .result__a").first
    link.wait_for(state="visible", timeout=20000)
    link.click()
    human_page.wait_for_load_state("domcontentloaded", timeout=30000)
    assert human_page.url.startswith("http")


@pytest.mark.e2e
@pytest.mark.network
def test_httpbin_form_sensitive_type(human_page):
    human_page.goto("https://httpbin.org/forms/post", wait_until="domcontentloaded", timeout=30000)
    human_page.locator('input[name="custname"]').click()
    human_page.keyboard.type("user@example.com", delay=20)
    human_page.locator('input[name="custtel"]').click()
    human_page.keyboard.type("secret-pass", delay=15)
    # Trang dùng <button>Submit order</button> (mặc định type=submit), không có type="submit" explicit
    human_page.get_by_role("button", name=re.compile(r"Submit order", re.I)).click()
    human_page.wait_for_load_state("domcontentloaded", timeout=20000)
    body = human_page.inner_text("body")
    assert "user@example.com" in body or "form" in body.lower()


@pytest.mark.e2e
@pytest.mark.network
def test_bot_sannysoft_smoke(human_page):
    human_page.goto("https://bot.sannysoft.com/", wait_until="domcontentloaded", timeout=60000)
    human_page.wait_for_timeout(9000)
    body = human_page.inner_text("body")
    # Bảng Intoli: đếm passed / failed thô
    passed_n = len(re.findall(r"\bpassed\b", body, re.I))
    wd = human_page.evaluate("() => navigator.webdriver")
    assert wd in (None, False)
    # Báo cáo trong assertion message (pytest -v hiện khi fail)
    assert passed_n >= 1, f"Không thấy passed nào. snippet={body[:800]!r}"
    # Headless vẫn có thể fail nhiều test — chỉ smoke: có dữ liệu bảng
    assert "WebDriver" in body or "webdriver" in body.lower()
