"""
Browser tool — fully automated Chrome management:
1. Auto-launch Chrome với remote debugging nếu chưa chạy
2. Connect vào Chrome đang chạy (giữ login, cookies, profile)
3. Anti-detection init scripts, human-like timing/mouse/typing, Multi-tab, Smart wait, Screenshot diff
"""
import base64
import os
import random
import subprocess
import sys
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from tools.human_behavior import HumanKeyboard, HumanMouse, HumanTiming

_pw = None
_context = None
_current_page = None
_pages: list = []

# ── Watchdog keep-alive ───────────────────────────────────────────────────────
_watchdog_thread: threading.Thread | None = None
_watchdog_stop = threading.Event()
_WATCHDOG_INTERVAL = 30  # seconds

# ── Resource blocking ─────────────────────────────────────────────────────────
_blocked_resource_types: set[str] = set()
_resource_blocking_active: bool = False

# ── Conversation-level browser context memory ─────────────────────────────────
# conversation_id → {"url": str, "visited": list, "fills": dict, "ts": float}
_browser_conv_state: dict[str, dict] = {}
_current_conv_id: str = ""

# ── Macro recording ───────────────────────────────────────────────────────────
_macro_recording: bool = False
_macro_steps: list[dict] = []
# site_key → list of recorded steps
_macro_library: dict[str, list[dict]] = {}

PROFILE_DIR = os.path.expanduser("~/.ai_agent_browser_profile")
CDP_PORT = int(os.getenv("CHROME_CDP_PORT", "9222") or 9222)
CDP_URL = os.getenv("CHROME_CDP_URL", f"http://localhost:{CDP_PORT}")

# Session export (cookies/localStorage snapshot) — bổ sung cho user_data_dir persistent.
# Dùng app_paths để tránh ghi vào bundle .app read-only khi chạy frozen.
from utils.app_paths import data_dir as _app_data_dir  # noqa: E402
STORAGE_PATH = _app_data_dir("browser_data") / "session.json"

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

# Per-session screen/DPI profiles — picked once at startup, consistent for the session
SCREEN_PROFILES = [
    {"width": 1920, "height": 1080, "dpr": 1},
    {"width": 2560, "height": 1440, "dpr": 2},
    {"width": 1440, "height": 900,  "dpr": 2},
    {"width": 1512, "height": 982,  "dpr": 2},
    {"width": 1280, "height": 800,  "dpr": 1},
]

_session_fingerprint: dict = {}


def _get_session_fingerprint() -> dict:
    global _session_fingerprint
    if not _session_fingerprint:
        _session_fingerprint = random.choice(SCREEN_PROFILES).copy()
    return _session_fingerprint


def _viewport() -> dict:
    w = os.getenv("BROWSER_VIEWPORT_W", "")
    h = os.getenv("BROWSER_VIEWPORT_H", "")
    if w and h:
        return {"width": int(w), "height": int(h)}
    fp = _get_session_fingerprint()
    return {"width": fp["width"], "height": fp["height"]}


def _headless() -> bool:
    return os.getenv("BROWSER_HEADLESS", "").lower() in ("1", "true", "yes")


# ── Page intent classifier → SSE (server drain sau mỗi tool) ─────────────────
PAGE_INTENT_SSE_QUEUE: list = []

# Cache kết quả classify: (url, dom_hash) → (timestamp, ClassifyResult)
# Tránh gọi vision mỗi action khi user đang ở cùng trang
_intent_cache: dict = {}
_INTENT_CACHE_TTL = 10.0  # seconds — đủ dài cho một flow navigate→fill→click
# URL của lần gate check cuối — dùng để skip gate nếu URL và DOM không đổi
_last_gate_url: str = ""
_last_gate_ts: float = 0.0
_GATE_SAME_URL_TTL = 8.0  # seconds — skip gate hoàn toàn nếu cùng URL trong window này
_intent_cache_lock = threading.Lock()  # Bảo vệ _intent_cache, _last_gate_url, _last_gate_ts


def push_page_intent_event(ev: dict) -> None:
    PAGE_INTENT_SSE_QUEUE.append(ev)


def drain_page_intent_events() -> list:
    global PAGE_INTENT_SSE_QUEUE
    out = list(PAGE_INTENT_SSE_QUEUE)
    PAGE_INTENT_SSE_QUEUE = []
    return out


# ── Browser frame preview → SSE ──────────────────────────────────────────────
# Emit sau navigate/click/fill để frontend render live preview
_BROWSER_FRAME_QUEUE: list = []
_BROWSER_FRAME_QUEUE_MAX = 20  # Giới hạn chống memory bloat
_last_frame_hash: int | None = None
_last_frame_ts: float = 0.0
_FRAME_COOLDOWN_MS = 400  # Min gap giữa 2 frame capture


def _capture_and_queue_frame(page) -> None:
    """Chụp screenshot trang hiện tại và đưa vào queue SSE.
    Dedupe theo hash + cooldown để tránh frame trùng lặp và memory bloat."""
    global _last_frame_hash, _last_frame_ts, _BROWSER_FRAME_QUEUE
    now_ms = time.time() * 1000
    if (now_ms - _last_frame_ts) < _FRAME_COOLDOWN_MS:
        return
    try:
        png_bytes = page.screenshot(type="png", timeout=4000)
        # Hash nhanh theo length + vài byte đầu/giữa/cuối
        h = hash((len(png_bytes), png_bytes[:64], png_bytes[len(png_bytes)//2:len(png_bytes)//2+64], png_bytes[-64:]))
        if h == _last_frame_hash:
            # Frame giống hệt lần trước — skip để tiết kiệm queue
            _last_frame_ts = now_ms
            return
        b64 = base64.standard_b64encode(png_bytes).decode()
        url = ""
        try:
            url = page.url or ""
        except Exception:
            pass
        _BROWSER_FRAME_QUEUE.append({"type": "browser_frame", "base64": b64, "url": url})
        # Giới hạn queue — drop các frame cũ nếu quá max
        if len(_BROWSER_FRAME_QUEUE) > _BROWSER_FRAME_QUEUE_MAX:
            _BROWSER_FRAME_QUEUE = _BROWSER_FRAME_QUEUE[-_BROWSER_FRAME_QUEUE_MAX:]
        _last_frame_hash = h
        _last_frame_ts = now_ms
    except Exception:
        pass


def drain_browser_frame_events() -> list:
    global _BROWSER_FRAME_QUEUE
    out = list(_BROWSER_FRAME_QUEUE)
    _BROWSER_FRAME_QUEUE = []
    return out


def _classifier_client_model():
    try:
        import server

        c = server.try_get_client()
        return c, server.DEFAULT_MODEL
    except Exception:
        return None, os.getenv("MODEL", "claude-sonnet-4-5")


def _emit_notable_intent(cr) -> None:
    from tools.page_classifier import PageIntent

    if cr.intent == PageIntent.READY and not cr.used_vision:
        return
    push_page_intent_event(
        {
            "intent": cr.intent.value,
            "message": (cr.reason or "")[:400],
            "suggested_action": cr.suggested_action,
            "confidence": round(float(cr.confidence), 4),
            "used_vision": cr.used_vision,
        }
    )


def _page_intent_gate(page) -> str | None:
    """
    Phân loại trạng thái trang; chặn action khi captcha/login/block/...
    Trả về chuỗi bắt đầu bằng 'Error:' hoặc None.
    Kết quả được cache theo (url, dom_hash) để tránh double-classify
    khi nhiều actions liên tiếp trên cùng trang.
    Skip hoàn toàn nếu cùng URL trong _GATE_SAME_URL_TTL giây.
    """
    global _last_gate_url, _last_gate_ts
    if os.getenv("PAGE_INTENT_CLASSIFIER", "1").lower() in ("0", "false", "no"):
        return None
    try:
        from tools.page_classifier import (
            PageIntent,
            classify_page_sync,
            should_block_action,
        )

        client, model = _classifier_client_model()
        purl = ""
        try:
            purl = page.url or ""
        except Exception:
            pass

        now = time.time()
        # Fast-skip: cùng URL và không quá _GATE_SAME_URL_TTL giây → bỏ qua gate
        with _intent_cache_lock:
            if purl and purl == _last_gate_url and (now - _last_gate_ts) < _GATE_SAME_URL_TTL:
                return None

        # Cache lookup: lấy 500 ký tự đầu body text làm key nhanh
        dom_snippet = ""
        try:
            dom_snippet = page.evaluate("document.body?.innerText?.slice(0,500) || ''") or ""
        except Exception:
            pass
        cache_key = (purl, hash(dom_snippet))
        with _intent_cache_lock:
            cached_entry = _intent_cache.get(cache_key)
        if cached_entry is not None:
            ts, cr = cached_entry
            if now - ts < _INTENT_CACHE_TTL:
                _emit_notable_intent(cr)
                result = should_block_action(cr, purl)
                if result is None:
                    with _intent_cache_lock:
                        _last_gate_url = purl
                        _last_gate_ts = now
                return result

        cr = classify_page_sync(page, client, model)
        with _intent_cache_lock:
            _intent_cache[cache_key] = (now, cr)
            # Giữ cache nhỏ — loại bỏ entry cũ nhất khi quá 32 entries
            if len(_intent_cache) > 32:
                oldest = min(_intent_cache, key=lambda k: _intent_cache[k][0])
                _intent_cache.pop(oldest, None)

        _emit_notable_intent(cr)
        msg = should_block_action(cr, purl)
        if msg:
            return msg

        if cr.intent == PageIntent.LOADING:
            try:
                page.wait_for_load_state("domcontentloaded", timeout=10000)
            except Exception:
                pass
            time.sleep(0.35)
            cr2 = classify_page_sync(page, client, model)
            with _intent_cache_lock:
                _intent_cache[cache_key] = (time.time(), cr2)
            _emit_notable_intent(cr2)
            return should_block_action(cr2, purl)

        _last_gate_url = purl
        _last_gate_ts = now
        return None
    except Exception:
        return None


# Một lần / context — tránh add_init_script trùng lặp
_init_scripts_applied_to: int | None = None


class BrowserCDPError(Exception):
    """CDP không bám được trong khi user đã cấu hình profile Chrome hệ thống — không mở Chrome fallback trắng."""


def _resolved_user_data_is_macos_main_chrome() -> bool:
    """True nếu đang trỏ vào đúng thư mục User Data của Chrome cài đặt chuẩn trên macOS."""
    ud, _ = _resolve_chrome_user_data_and_profile()
    ud = os.path.normpath(os.path.expanduser(ud))
    if sys.platform != "darwin":
        return False
    main = os.path.normpath(os.path.expanduser("~/Library/Application Support/Google/Chrome"))
    return ud == main


def _wants_system_chrome_profile() -> bool:
    """
    Chế độ không dùng Playwright fallback: chỉ khi bạn cố dùng chung User Data với Chrome hàng ngày.
    Thư mục riêng (vd. ~/.ai_agent_browser_profile hoặc CHROME_USER_DATA_DIR tùy chỉnh khác Chrome chính)
    không bị coi là «hệ thống» — có thể fallback và chạy song song Chrome cá nhân.
    """
    if os.getenv("CHROME_SHARE_SYSTEM_PROFILE", "").lower() in ("1", "true", "yes"):
        return True
    return _resolved_user_data_is_macos_main_chrome()


# Tránh spawn song song; RLock để _get_page có thể gọi _ensure_chrome_debug bên trong cùng lock
_browser_launch_lock = threading.RLock()

# Chỉ Popen Chrome + --remote-debugging-port MỘT LẦN / phiên server.
# Nếu không, mỗi lần gọi browser_* lại spawn → spam cửa sổ (đặc biệt khi Chrome đã mở tay không có CDP).
_cdp_chrome_popen_done = False
# Playwright launch_persistent chỉ một lần (fallback khi CDP không bám được)
_playwright_persistent_launched = False


def _resolve_chrome_user_data_and_profile():
    """
    Thư mục User Data + tên profile con (vd. Default, Profile 1).
    Mặc định dùng ~/.ai_agent_browser_profile để CDP và Playwright fallback
    cùng một thư mục — tránh mở «hai Chrome» (một từ CDP, một từ launch_persistent).
    Muốn dùng chung cookie với Chrome hàng ngày: CHROME_SHARE_SYSTEM_PROFILE=1 (xung đột nếu Chrome đang mở).
    Muốn giữ Chrome cá nhân đang mở nhiều profile: không bật SHARE; agent dùng thư mục riêng ở đây.
    """
    override = (os.getenv("CHROME_USER_DATA_DIR") or os.getenv("BROWSER_USER_DATA_DIR") or "").strip()
    if override:
        user_data_dir = os.path.expanduser(override)
    elif os.getenv("CHROME_SHARE_SYSTEM_PROFILE", "").lower() in ("1", "true", "yes"):
        user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
        if not os.path.exists(user_data_dir):
            user_data_dir = PROFILE_DIR
    else:
        user_data_dir = PROFILE_DIR
    profile = (os.getenv("CHROME_PROFILE_DIRECTORY") or "Default").strip() or "Default"
    return user_data_dir, profile

ANTI_DETECTION_INIT = """
(() => {
  try {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined, configurable: true });

    // Fake PluginArray giống Chrome macOS thật (không phải số nguyên)
    const _fakeMimeType = (type, desc, suffixes) => ({ type, description: desc, suffixes, enabledPlugin: null });
    const _fakePlugin = (name, filename, desc, mimes) => {
      const p = { name, filename, description: desc, length: mimes.length };
      mimes.forEach((m, i) => { p[i] = m; });
      p[Symbol.iterator] = function*() { for(let i=0;i<this.length;i++) yield this[i]; };
      return p;
    };
    const _plugins = [
      _fakePlugin('Chrome PDF Plugin',        'internal-pdf-viewer',  'Portable Document Format', [_fakeMimeType('application/x-google-chrome-pdf','Portable Document Format','pdf')]),
      _fakePlugin('Chrome PDF Viewer',        'mhjfbmdgcfjbbpaeojofohoefgiehjai','',              [_fakeMimeType('application/pdf','','pdf')]),
      _fakePlugin('Native Client',            'internal-nacl-plugin', '',                         [_fakeMimeType('application/x-nacl','Native Client Executable',''),_fakeMimeType('application/x-pnacl','Portable Native Client Executable','')]),
    ];
    Object.defineProperty(navigator, 'plugins', {
      get: () => Object.assign(_plugins, { length: _plugins.length, item: i => _plugins[i], namedItem: n => _plugins.find(p=>p.name===n)||null, [Symbol.iterator]: function*(){ yield* _plugins; } }),
      configurable: true,
    });

    Object.defineProperty(navigator, 'languages', { get: () => ['vi-VN', 'vi', 'en-US', 'en'], configurable: true });
    window.chrome = { runtime: {}, loadTimes: function(){}, csi: function(){}, app: {} };
    const orig = window.navigator.permissions && window.navigator.permissions.query;
    if (orig) {
      window.navigator.permissions.query = (p) =>
        p.name === 'notifications' ? Promise.resolve({ state: Notification.permission }) : orig(p);
    }
  } catch (e) {}

  // Canvas 2D: noise on fillText + getImageData
  try {
    const originalGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(type, ...args) {
      const ctx = originalGetContext.call(this, type, ...args);
      if (type === '2d' && ctx) {
        const origFillText = ctx.fillText.bind(ctx);
        ctx.fillText = function(...a) {
          ctx.shadowBlur = Math.random() * 0.08;
          return origFillText(...a);
        };
        const origGetImageData = ctx.getImageData.bind(ctx);
        ctx.getImageData = function(x, y, w, h) {
          const d = origGetImageData(x, y, w, h);
          for (let i = 0; i < d.data.length; i += 200) {
            d.data[i] = d.data[i] ^ (Math.random() * 2 | 0);
          }
          return d;
        };
        const origStrokeText = ctx.strokeText.bind(ctx);
        ctx.strokeText = function(...a) {
          ctx.shadowBlur = Math.random() * 0.05;
          return origStrokeText(...a);
        };
      }
      return ctx;
    };
  } catch (e) {}

  // WebGL: Apple GPU strings + noise on getParameter
  try {
    const _patchWebGL = (Cls) => {
      if (typeof Cls === 'undefined') return;
      const orig = Cls.prototype.getParameter;
      Cls.prototype.getParameter = function(p) {
        if (p === 37445) return 'Apple Inc.';
        if (p === 37446) return 'Apple GPU';
        return orig.call(this, p);
      };
      const origReadPixels = Cls.prototype.readPixels;
      Cls.prototype.readPixels = function(...args) {
        const r = origReadPixels.apply(this, args);
        if (args[6] instanceof Uint8Array) {
          args[6][0] = args[6][0] ^ (Math.random() * 2 | 0);
        }
        return r;
      };
    };
    _patchWebGL(WebGLRenderingContext);
    if (typeof WebGL2RenderingContext !== 'undefined') _patchWebGL(WebGL2RenderingContext);
  } catch (e) {}

  // Audio fingerprint: AnalyserNode noise
  try {
    const origGetFloatFrequencyData = AnalyserNode.prototype.getFloatFrequencyData;
    AnalyserNode.prototype.getFloatFrequencyData = function(arr) {
      origGetFloatFrequencyData.call(this, arr);
      for (let i = 0; i < arr.length; i += 100) {
        arr[i] += (Math.random() - 0.5) * 0.0001;
      }
    };
  } catch (e) {}

  // performance.now jitter — chống timing attacks
  try {
    const origNow = Performance.prototype.now;
    Performance.prototype.now = function() {
      return origNow.call(this) + (Math.random() * 0.1 - 0.05);
    };
  } catch (e) {}

  // Screen properties — macOS Retina 1440×900
  try {
    Object.defineProperty(screen, 'width',       { get: () => 1440, configurable: true });
    Object.defineProperty(screen, 'height',      { get: () => 900,  configurable: true });
    Object.defineProperty(screen, 'availWidth',  { get: () => 1440, configurable: true });
    Object.defineProperty(screen, 'availHeight', { get: () => 900,  configurable: true });
    Object.defineProperty(screen, 'colorDepth',  { get: () => 24,   configurable: true });
    Object.defineProperty(screen, 'pixelDepth',  { get: () => 24,   configurable: true });
    Object.defineProperty(window, 'devicePixelRatio', { get: () => 2, configurable: true });
  } catch (e) {}

  // Spoof connection as fast WiFi
  try {
    if (navigator.connection) {
      Object.defineProperty(navigator.connection, 'rtt',             { get: () => 50,       configurable: true });
      Object.defineProperty(navigator.connection, 'downlink',        { get: () => 10,       configurable: true });
      Object.defineProperty(navigator.connection, 'effectiveType',   { get: () => '4g',     configurable: true });
      Object.defineProperty(navigator.connection, 'saveData',        { get: () => false,    configurable: true });
    }
  } catch (e) {}
})();
"""


def _apply_anti_detection_init(context) -> None:
    global _init_scripts_applied_to
    cid = id(context)
    if _init_scripts_applied_to == cid:
        return
    try:
        context.add_init_script(ANTI_DETECTION_INIT)
        # Override screen dimensions with per-session randomized fingerprint
        fp = _get_session_fingerprint()
        screen_override = f"""
(() => {{
  try {{
    Object.defineProperty(screen, 'width',       {{ get: () => {fp['width']},  configurable: true }});
    Object.defineProperty(screen, 'height',      {{ get: () => {fp['height']}, configurable: true }});
    Object.defineProperty(screen, 'availWidth',  {{ get: () => {fp['width']},  configurable: true }});
    Object.defineProperty(screen, 'availHeight', {{ get: () => {fp['height'] - 40}, configurable: true }});
    Object.defineProperty(window, 'devicePixelRatio', {{ get: () => {fp['dpr']}, configurable: true }});
  }} catch (e) {{}}
}})();
"""
        context.add_init_script(screen_override)
        _init_scripts_applied_to = cid
    except Exception:
        pass


def _watchdog_loop() -> None:
    """Ping browser mỗi _WATCHDOG_INTERVAL giây; tự reconnect nếu crash."""
    global _pw, _context, _current_page, _pages, _init_scripts_applied_to
    global _playwright_persistent_launched, _cdp_chrome_popen_done
    while not _watchdog_stop.wait(_WATCHDOG_INTERVAL):
        try:
            page = _current_page
            if page is None:
                continue
            page.evaluate("1")
        except Exception:
            print("[Browser watchdog] Phát hiện browser crash — đang reconnect...")
            with _browser_launch_lock:
                _pw = None
                _context = None
                _current_page = None
                _pages = []
                _init_scripts_applied_to = None
                _playwright_persistent_launched = False
                _cdp_chrome_popen_done = False
            try:
                _get_page()
                print("[Browser watchdog] Reconnect thành công.")
            except Exception as e:
                print(f"[Browser watchdog] Reconnect thất bại: {e}")


def _start_watchdog() -> None:
    global _watchdog_thread
    if _watchdog_thread is not None and _watchdog_thread.is_alive():
        return
    _watchdog_stop.clear()
    _watchdog_thread = threading.Thread(target=_watchdog_loop, daemon=True, name="browser-watchdog")
    _watchdog_thread.start()


def _apply_resource_blocking(page) -> None:
    """Áp dụng resource blocking cho page dựa trên _blocked_resource_types."""
    if not _resource_blocking_active or not _blocked_resource_types:
        return
    try:
        def _handle_route(route, request):
            if request.resource_type in _blocked_resource_types:
                route.abort()
            else:
                route.continue_()
        try:
            page.unroute("**/*")
        except Exception:
            pass
        page.route("**/*", _handle_route)
    except Exception:
        pass


def _register_dialog_handler(page) -> None:
    """
    Đăng ký auto-handler cho browser dialogs (alert/confirm/prompt/beforeunload).
    - alert/confirm: tự accept để tránh Playwright bị treo
    - prompt: dismiss (không nhập text tùy tiện)
    - beforeunload: accept để thoát page bình thường
    Emit SSE event để frontend biết dialog đã xuất hiện.
    """
    def _on_dialog(dialog) -> None:
        dtype = dialog.type  # "alert" | "confirm" | "prompt" | "beforeunload"
        msg = (dialog.message or "")[:200]
        try:
            if dtype in ("alert", "confirm", "beforeunload"):
                dialog.accept()
            else:
                dialog.dismiss()
        except Exception:
            pass
        push_page_intent_event({
            "intent": "dialog",
            "message": f"[{dtype}] {msg}",
            "suggested_action": "proceed",
            "confidence": 1.0,
            "used_vision": False,
        })
    try:
        page.on("dialog", _on_dialog)
    except Exception:
        pass


def save_browser_session(context) -> None:
    """Lưu storage_state (cookies, origins) ra file — gọi trước khi đóng context."""
    try:
        STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path=str(STORAGE_PATH))
    except Exception:
        pass


def _load_storage_state_path() -> str | None:
    if STORAGE_PATH.exists():
        return str(STORAGE_PATH)
    return None


def _apply_storage_state_to_cdp_context(ctx) -> None:
    """Inject cookies + localStorage từ storage_state vào CDP context (vì attach CDP không nhận arg storage_state).
    Giúp giữ login khi watchdog reconnect hoặc restart server."""
    if not STORAGE_PATH.exists():
        return
    try:
        import json as _json
        with open(STORAGE_PATH, "r", encoding="utf-8") as f:
            state = _json.load(f)
    except Exception:
        return
    # Cookies — Playwright chấp nhận trực tiếp format {name, value, domain, ...}
    cookies = state.get("cookies") or []
    if cookies:
        try:
            ctx.add_cookies(cookies)
        except Exception as e:
            print(f"[Browser] Không inject được cookies vào CDP context: {e}")
    # localStorage — chỉ inject khi có page hiện đang mở origin tương ứng (tránh mở hàng loạt tab)
    origins = state.get("origins") or []
    if origins and ctx.pages:
        try:
            for origin in origins:
                origin_url = origin.get("origin")
                kvs = origin.get("localStorage") or []
                if not origin_url or not kvs:
                    continue
                for p in ctx.pages:
                    try:
                        if p.url.startswith(origin_url):
                            for kv in kvs:
                                k, v = kv.get("name"), kv.get("value")
                                if k is None or v is None:
                                    continue
                                p.evaluate(
                                    "({k,v}) => localStorage.setItem(k, v)",
                                    {"k": k, "v": v},
                                )
                            break
                    except Exception:
                        continue
        except Exception:
            pass

def _find_chrome_binary():
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def _is_chrome_debug_running() -> bool:
    """Kiểm tra Chrome debug port có đang mở không."""
    import urllib.request
    try:
        urllib.request.urlopen(f"http://localhost:{CDP_PORT}/json/version", timeout=1)
        return True
    except Exception:
        return False


def _launch_chrome_with_debug():
    """Mở tối đa MỘT process Chrome có CDP; các lần sau chỉ poll port (không Popen lại)."""
    global _cdp_chrome_popen_done
    chrome_bin = _find_chrome_binary()
    if not chrome_bin:
        return False

    user_data_dir, profile_dir = _resolve_chrome_user_data_and_profile()

    # Xóa SingletonLock nếu còn sót từ lần trước (Chrome crash / kill đột ngột)
    singleton_lock = os.path.join(user_data_dir, "SingletonLock")
    singleton_socket = os.path.join(user_data_dir, "SingletonSocket")
    for lock_file in (singleton_lock, singleton_socket):
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
                print(f"[Browser] Đã xóa lock file: {lock_file}")
        except Exception:
            pass

    if not _cdp_chrome_popen_done:
        _cdp_chrome_popen_done = True
        cmd = [
            chrome_bin,
            f"--remote-debugging-port={CDP_PORT}",
            f"--user-data-dir={user_data_dir}",
            f"--profile-directory={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--no-session-restore",          # không restore tab cũ
            "--restore-last-session=false",   # tắt restore session
            "--disable-session-crashed-bubble",
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-infobars",
            "--window-size=1440,900",
            "--start-maximized",
            "--exclude-switches=enable-automation",
            "--disable-automation",
            "about:blank",                    # mở 1 tab sạch thay vì restore
        ]
        try:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("[Browser] Đã khởi chạy Chrome (CDP) — không spawn thêm process Chrome trong phiên server.")
        except Exception as ex:
            print(f"[Browser] Không thể spawn Chrome: {ex}")

    # Đợi port (kể cả Chrome đã mở từ lần trước hoặc user tự bật CDP)
    for _ in range(28):
        time.sleep(0.35)
        if _is_chrome_debug_running():
            return True
    return _is_chrome_debug_running()


def _ensure_chrome_debug():
    """Gọi từ _get_page khi đã giữ _browser_launch_lock — tối đa một lần Popen Chrome CDP."""
    if _is_chrome_debug_running():
        return True
    print("[Browser] Port CDP chưa có — khởi động / đợi Chrome (một lần)...")
    ok = _launch_chrome_with_debug()
    if ok:
        print(f"[Browser] Chrome debug sẵn sàng tại port {CDP_PORT}")
    else:
        print(
            "[Browser] Port CDP không lên — có thể Chrome đang mở sẵn không có remote-debugging, "
            "hoặc profile đang khóa. Sẽ thử Playwright profile riêng (không spawn Chrome CDP lại)."
        )
    return ok


def launch_chrome_gui_without_picker() -> str:
    """open_app("Chrome") — cùng luồng CDP một lần, không Popen lặp."""
    if _is_chrome_debug_running():
        return (
            "Chrome automation đã chạy (remote debugging). "
            "Dùng browser_navigate để mở URL — không cần mở thêm Chrome."
        )
    with _browser_launch_lock:
        if _is_chrome_debug_running():
            return "Chrome automation đã sẵn sàng. Dùng browser_navigate để mở URL."
        ok = _launch_chrome_with_debug()
    time.sleep(0.5)
    if ok:
        return (
            "Đã khởi động Chrome cho agent (cùng profile với browser_*). "
            "Dùng browser_navigate để mở trang."
        )
    return (
        "Error: Port CDP chưa sẵn sàng. Đóng hết cửa sổ Chrome rồi thử lại, "
        "hoặc kiểm tra profile không bị khóa bởi Chrome đang mở tay."
    )


def _get_page():
    global _pw, _context, _current_page, _pages, _playwright_persistent_launched
    global _init_scripts_applied_to

    # Giữ lock khi check page liveness để tránh race với thread khác close page
    with _browser_launch_lock:
        if _current_page is not None:
            try:
                _current_page.title()
                # Verify page vẫn attached vào _context (tránh stale reference)
                try:
                    if _context is not None and _current_page.context != _context:
                        raise RuntimeError("page detached from tracked context")
                except Exception:
                    raise
                return _current_page
            except Exception:
                # Đóng gracefully tất cả pages trong context cũ trước khi reset tracking,
                # tránh leak handle khi reconnect (nhất là sau crash/watchdog restart).
                old_ctx = _context
                _current_page = None
                _pages = []
                _context = None
                _playwright_persistent_launched = False
                _init_scripts_applied_to = None
                if old_ctx is not None:
                    try:
                        for _p in list(old_ctx.pages):
                            try:
                                _p.close()
                            except Exception:
                                pass
                    except Exception:
                        pass

    if _pw is None:
        _pw = sync_playwright().start()

    user_data_dir, profile_subdir = _resolve_chrome_user_data_and_profile()
    os.makedirs(user_data_dir, exist_ok=True)

    with _browser_launch_lock:
        # Đảm bảo Chrome debug đang chạy (tự mở nếu cần)
        _ensure_chrome_debug()

        # Thử CDP vài lần (Chrome đôi khi chậm mở port — tránh nhảy sang launch_persistent tạo Chrome thứ hai)
        browser = None
        for attempt in range(8):
            if not _is_chrome_debug_running():
                time.sleep(0.35)
                continue
            try:
                browser = _pw.chromium.connect_over_cdp(CDP_URL, timeout=8000)
                break
            except Exception as e:
                print(f"[Browser] CDP connect attempt {attempt + 1}: {e}")
                time.sleep(0.5)

        if browser is not None:
            try:
                contexts = browser.contexts
                if contexts:
                    ctx = contexts[0]
                    pages = ctx.pages
                    # Đóng các blank tabs thừa, chỉ giữ 1
                    if len(pages) > 1:
                        blank_tabs = [p for p in pages if p.url in ('about:blank', '')]
                        keep = pages[0]
                        for p in blank_tabs:
                            if p != keep:
                                try:
                                    p.close()
                                except Exception:
                                    pass
                        pages = ctx.pages
                    page = pages[0] if pages else ctx.new_page()
                    _context = ctx
                    _current_page = page
                    _pages = list(ctx.pages) or [page]
                    _apply_anti_detection_init(ctx)
                    # Inject cookies/localStorage từ session trước (quan trọng sau watchdog reconnect)
                    _apply_storage_state_to_cdp_context(ctx)
                    _register_dialog_handler(_current_page)
                    try:
                        vp = _viewport()
                        _current_page.set_viewport_size(vp)
                    except Exception:
                        pass
                    return _current_page
            except Exception as e:
                print(f"[Browser] CDP attach contexts failed: {e}, dùng fallback")

        # Chỉ khi đang share đúng User Data Chrome chính: không fallback sang profile agent (tránh hai cửa sổ nhầm chỗ).
        if _wants_system_chrome_profile():
            raise BrowserCDPError(
                f"Không kết nối được tới Chrome qua CDP (port {CDP_PORT}) với thư mục User Data Chrome bạn đang dùng chung với Chrome hàng ngày. "
                "Trong chế độ này agent không mở thêm Chrome profile riêng (~/.ai_agent_browser_profile).\n\n"
                "Nếu bạn cần giữ Chrome đang mở nhiều profile khác: trong .env hãy tắt CHROME_SHARE_SYSTEM_PROFILE "
                "(và bỏ CHROME_USER_DATA_DIR trỏ vào ~/Library/.../Google/Chrome nếu có). "
                "Agent sẽ dùng thư mục riêng ~/.ai_agent_browser_profile — chạy song song, không bắt thoát Chrome cá nhân "
                "(bạn đăng nhập lại site trong cửa sổ agent nếu cần).\n\n"
                "Nếu vẫn muốn đúng một profile hệ thống: thoát hẳn Google Chrome (⌘Q) rồi chạy lại task để agent mở Chrome có remote debugging."
            )

        # Mặc định (không share profile hệ thống): fallback một Chrome Playwright profile riêng
        os.makedirs(PROFILE_DIR, exist_ok=True)
        # Xóa SingletonLock trong profile riêng nếu còn sót
        for _lf in ("SingletonLock", "SingletonSocket", "lockfile"):
            _lp = os.path.join(PROFILE_DIR, _lf)
            try:
                if os.path.exists(_lp):
                    os.remove(_lp)
            except Exception:
                pass
        print(
            "[Browser] CDP không bám được — mở Playwright một lần với ~/.ai_agent_browser_profile "
            "(chỉ khi không dùng CHROME_SHARE_SYSTEM_PROFILE)."
        )
        chrome_bin = _find_chrome_binary()
        vp = _viewport()
        launch_kwargs = dict(
            user_data_dir=PROFILE_DIR,
            headless=_headless(),
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
                "--start-maximized",
                "--exclude-switches=enable-automation",
                "--disable-automation",
                "--profile-directory=Default",
            ],
            ignore_default_args=["--enable-automation", "--enable-blink-features=IdleDetection"],
        )
        ss = _load_storage_state_path()
        if ss:
            launch_kwargs["storage_state"] = ss
        if chrome_bin:
            launch_kwargs["executable_path"] = chrome_bin

        _context = _pw.chromium.launch_persistent_context(**launch_kwargs)
        _playwright_persistent_launched = True
        _apply_anti_detection_init(_context)
        _current_page = _context.pages[0] if _context.pages else _context.new_page()
        _pages = [_current_page]
        try:
            _current_page.set_viewport_size(vp)
        except Exception:
            pass
        _apply_resource_blocking(_current_page)
        _register_dialog_handler(_current_page)
        _start_watchdog()
        return _current_page


# ── DOM stability check cho SPA (React/Vue/Angular hydration) ──
def _wait_for_dom_stable(page, timeout_ms: int = 1000) -> None:
    """
    Chờ DOM ngưng thay đổi — phát hiện SPA đã hoàn tất hydration.
    Dùng MutationObserver: resolve sau 200ms không có mutations.
    Không throw nếu timeout — chỉ best-effort.
    """
    js = """
    (timeoutMs) => new Promise(resolve => {
        let timer;
        const reset = () => {
            clearTimeout(timer);
            timer = setTimeout(() => { obs.disconnect(); resolve(true); }, 200);
        };
        const obs = new MutationObserver(reset);
        obs.observe(document.body || document.documentElement, {
            childList: true, subtree: true, attributes: true, characterData: true
        });
        reset();
        setTimeout(() => { obs.disconnect(); resolve(false); }, timeoutMs);
    })
    """
    try:
        page.evaluate(js, timeout_ms)
    except Exception:
        pass


# ── Smart wait ──
def smart_wait(page, timeout=15000):
    """Đợi content thực sự load: thử networkidle 2s, fallback domcontentloaded, rồi check spinners."""
    try:
        page.wait_for_load_state("networkidle", timeout=2000)
    except Exception:
        try:
            page.wait_for_load_state("domcontentloaded", timeout=timeout)
        except Exception:
            pass
    for spinner in [".loading", "#loading", "[data-loading]", ".spinner"]:
        try:
            page.wait_for_selector(spinner, state="hidden", timeout=800)
        except Exception:
            pass


def _detect_block_or_captcha(page) -> tuple:
    """Phát hiện trang chặn/CAPTCHA — trả (blocked: bool, reason: str)."""
    try:
        url = (page.url or "").lower()
        snippet = (page.content() or "")[:120000].lower()
    except Exception:
        return False, ""
    checks = [
        ("cf-browser-verification", "Cloudflare challenge"),
        ("attention required", "Trang chặn (Cloudflare / attention)"),
        ("recaptcha", "reCAPTCHA"),
        ("hcaptcha", "hCaptcha"),
        ("captcha", "CAPTCHA"),
        ("unusual traffic", "Google unusual traffic"),
        ("verify you are human", "Yêu cầu xác minh người dùng"),
        ("are you a robot", "Thử thách robot"),
    ]
    for needle, label in checks:
        if needle in url or needle in snippet:
            return True, label
    return False, ""


# ── Screenshot diff ──
def screenshot_diff(before_b64: str, after_b64: str) -> dict:
    """So sánh 2 ảnh base64 bằng PIL. Trả về changed, change_percent, description."""
    try:
        from PIL import Image, ImageChops
        import io, math

        before_bytes = base64.b64decode(before_b64)
        after_bytes = base64.b64decode(after_b64)
        img_before = Image.open(io.BytesIO(before_bytes)).convert("RGB")
        img_after = Image.open(io.BytesIO(after_bytes)).convert("RGB")

        # Resize to same size if needed
        if img_before.size != img_after.size:
            img_after = img_after.resize(img_before.size)

        diff = ImageChops.difference(img_before, img_after)
        pixels = list(diff.getdata())
        total = len(pixels)
        changed_pixels = sum(1 for p in pixels if any(c > 10 for c in p))
        change_percent = (changed_pixels / total) * 100 if total > 0 else 0.0
        changed = change_percent > 5.0
        description = f"{'Có thay đổi' if changed else 'Không thay đổi'} ({change_percent:.1f}% pixels thay đổi)"
        return {"changed": changed, "change_percent": round(change_percent, 2), "description": description}
    except Exception as e:
        return {"changed": False, "change_percent": 0.0, "description": f"Không thể so sánh: {e}"}


# ── Multi-tab support ──
def new_tab(url: str = "") -> str:
    """Mở tab mới, trả về tab_id (index)."""
    global _current_page, _pages
    try:
        _get_page()  # ensure context is initialized
    except BrowserCDPError as e:
        return f"Error: {e}"
    page = _context.new_page()
    try:
        page.set_viewport_size(_viewport())
    except Exception:
        pass
    _register_dialog_handler(page)
    _pages.append(page)
    tab_id = len(_pages) - 1
    _current_page = page
    if url:
        try:
            page.goto(url, timeout=30000)
            smart_wait(page)
        except Exception as e:
            return f"Tab {tab_id} opened but navigation failed: {e}"
    return f"Opened tab {tab_id}" + (f" at {url}" if url else "")


def switch_tab(tab_id: int) -> str:
    """Chuyển sang tab theo index."""
    global _current_page
    try:
        _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    if tab_id < 0 or tab_id >= len(_pages):
        return f"Error: tab_id {tab_id} không tồn tại (có {len(_pages)} tabs)"
    try:
        candidate = _pages[tab_id]
        candidate.title()  # check alive
        # Verify page vẫn attached vào context hiện tại (CDP có thể đã tái sử dụng tab)
        if _context is not None and candidate.context != _context:
            # Rebuild _pages từ context thực tế rồi thử lại
            _pages[:] = list(_context.pages)
            if tab_id >= len(_pages):
                return f"Error: tab {tab_id} không còn tồn tại trong context (chỉ có {len(_pages)} tabs)"
            candidate = _pages[tab_id]
            candidate.title()
        _current_page = candidate
        _current_page.bring_to_front()
        return f"Switched to tab {tab_id}: {_current_page.url}"
    except Exception as e:
        return f"Error switching to tab {tab_id}: {e}"


def close_tab(tab_id: int) -> str:
    """Đóng tab theo index."""
    global _current_page, _pages
    try:
        _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    if tab_id < 0 or tab_id >= len(_pages):
        return f"Error: tab_id {tab_id} không tồn tại"
    try:
        page = _pages[tab_id]
        page.close()
        _pages.pop(tab_id)
        if not _pages:
            _current_page = None
        elif _current_page == page:
            _current_page = _pages[max(0, tab_id - 1)]
        return f"Closed tab {tab_id}"
    except Exception as e:
        return f"Error closing tab {tab_id}: {e}"


def list_tabs() -> str:
    """Liệt kê tất cả tabs đang mở."""
    try:
        _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    result = []
    for i, page in enumerate(_pages):
        try:
            title = page.title()
            url = page.url
            active = " [active]" if page == _current_page else ""
            result.append(f"Tab {i}{active}: {title} — {url}")
        except Exception:
            result.append(f"Tab {i}: [closed]")
    return "\n".join(result) if result else "Không có tab nào"


def navigate(url: str, wait_for: str = "load") -> str:
    global _last_gate_url, _last_gate_ts
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    try:
        HumanTiming.think(300, 700)
        # Reset gate cache khi navigate sang URL mới
        try:
            current_url = page.url or ""
        except Exception:
            current_url = ""
        if current_url != url:
            _last_gate_url = ""
            _last_gate_ts = 0.0
        page.goto(url, wait_until=wait_for, timeout=30000)
        smart_wait(page)
        _wait_for_dom_stable(page)
        HumanTiming.after_navigate()
        read_time = random.uniform(0.3, 0.7)
        HumanMouse.idle_movement(page, read_time)
        gate_err = _page_intent_gate(page)
        if gate_err:
            return gate_err
        title = page.title()
        blocked, reason = _detect_block_or_captcha(page)
        msg = f"Đã navigate: url={page.url} title={title}"
        if blocked:
            msg += f"\nCảnh báo: có dấu hiệu chặn hoặc CAPTCHA ({reason}). Dừng lại và báo cho user — không cố bypass tự động."
        _capture_and_queue_frame(page)
        _record_macro_step("navigate", url=url)
        _update_browser_conv_state("navigate", url=page.url)
        return msg
    except Exception as e:
        return f"Error navigating to {url}: {e}"


def get_text() -> str:
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    for selector in ["main", "article", "#main", ".main", "body"]:
        try:
            text = page.inner_text(selector, timeout=5000)
            if text.strip():
                return text[:5000]
        except Exception:
            continue
    return ""


def get_element_text(selector: str) -> str:
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    try:
        return page.inner_text(selector, timeout=5000)[:3000]
    except Exception as e:
        return f"Không tìm thấy element: {e}"


def get_page_title() -> str:
    try:
        return _get_page().title()
    except BrowserCDPError as e:
        return f"Error: {e}"


def _try_click_element(page, element, label: str) -> str | None:
    """
    Thực hiện click vào element đã locate. Thử scroll_into_view → bounding_box → HumanMouse click.
    Trả về chuỗi kết quả nếu thành công, None nếu fail.
    """
    try:
        element.scroll_into_view_if_needed(timeout=5000)
        box = element.bounding_box()
        if not box:
            return None
        click_x = int(box["x"] + box["width"] * random.uniform(0.3, 0.7))
        click_y = int(box["y"] + box["height"] * random.uniform(0.3, 0.7))
        HumanTiming.think(200, 500)
        HumanMouse.click(page, click_x, click_y)
        HumanTiming.after_click()
        blocked, reason = _detect_block_or_captcha(page)
        out = f"Đã click ({label})"
        if blocked:
            out += f"\nCảnh báo: {reason}"
        _capture_and_queue_frame(page)
        _record_macro_step("click", text=label if label.startswith("text=") else None,
                           selector=label if not label.startswith("text=") and not label.startswith("role=") else None)
        return out
    except Exception:
        return None


def click_selector(selector: str | None = None, text: str | None = None) -> str:
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    sel = (selector or "").strip()
    txt = (text or "").strip()
    if not sel and not txt:
        return "Error: Cần `selector` hoặc `text` để click."
    try:
        gate_err = _page_intent_gate(page)
        if gate_err:
            return gate_err

        # Strategy 1: CSS selector trực tiếp
        if sel:
            result = _try_click_element(page, page.locator(sel).first, sel)
            if result:
                return result

        # Strategy 2: text locator (exact=False)
        if txt:
            result = _try_click_element(page, page.get_by_text(txt, exact=False).first, f"text={txt!r}")
            if result:
                return result

        # Strategy 3: role-based (button/link có text) — loại bỏ disabled element
        if txt:
            for role in ("button", "link", "menuitem", "tab", "option"):
                try:
                    loc = page.get_by_role(role, name=txt).filter(
                        has_not=page.locator('[aria-disabled="true"], [disabled]')
                    )
                    if _locator_ready(loc, 800):
                        result = _try_click_element(page, loc.first, f"role={role} name={txt!r}")
                        if result:
                            return result
                except Exception:
                    continue

        # Strategy 4: aria-label / placeholder / title attribute
        if txt:
            for attr in ("aria-label", "placeholder", "title", "alt"):
                try:
                    loc = page.locator(f"[{attr}*='{txt}' i]")
                    if _locator_ready(loc, 600):
                        result = _try_click_element(page, loc.first, f"[{attr}~={txt!r}]")
                        if result:
                            return result
                except Exception:
                    continue

        # Strategy 4b: iframe / shadow DOM — nhiều site (Stripe, reCAPTCHA, YouTube embed) để button trong iframe
        if sel or txt:
            for label, iloc in _iframe_locators(page, sel, txt):
                try:
                    if _locator_ready(iloc, 600):
                        result = _try_click_element(page, iloc.first, label)
                        if result:
                            return result
                except Exception:
                    continue

        # Strategy 5: scroll down + retry selector/text (element có thể chưa vào viewport)
        label_for_err = sel or txt
        page.mouse.wheel(0, 400)
        time.sleep(0.4)
        if sel:
            result = _try_click_element(page, page.locator(sel).first, f"{sel} (after scroll)")
            if result:
                return result
        if txt:
            result = _try_click_element(page, page.get_by_text(txt, exact=False).first, f"text={txt!r} (after scroll)")
            if result:
                return result

        # Strategy 6: vision fallback
        if txt:
            try:
                from tools.vision_dom import HybridBrowserExecutor
                from tools.browser import _classifier_client_model
                client, model = _classifier_client_model()
                if client:
                    vision_result = HybridBrowserExecutor.smart_click(
                        page, txt, sel or None, client, model, verify=False
                    )
                    if isinstance(vision_result, dict) and vision_result.get("success"):
                        _capture_and_queue_frame(page)
                        return f"Đã click (vision: {txt!r})"
            except Exception:
                pass

        err_msg = f"Error: Không tìm thấy element để click — đã thử selector/text/role/aria/scroll/vision ({label_for_err!r})"
        try:
            _screenshot_on_error(page, f"click_failed:{label_for_err}")
        except Exception:
            pass
        return err_msg
    except Exception as e:
        return f"Error clicking {sel or txt}: {e}"


def fill(selector: str, value: str, sensitive: bool = False) -> str:
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    try:
        gate_err = _page_intent_gate(page)
        if gate_err:
            return gate_err
        HumanTiming.think(300, 600)
        if sensitive:
            locator = page.locator(selector).first
            locator.click(timeout=10000)
            time.sleep(random.uniform(0.1, 0.2))
            # Clear field trước khi gõ (tránh append vào text có sẵn)
            try:
                locator.fill("", timeout=3000)
            except Exception:
                # Fallback: select-all + delete
                try:
                    import platform as _p
                    modifier = "Meta" if _p.system() == "Darwin" else "Control"
                    page.keyboard.press(f"{modifier}+A")
                    time.sleep(0.05)
                    page.keyboard.press("Backspace")
                except Exception:
                    pass
            page.keyboard.type(value, delay=random.uniform(50, 100))
        else:
            HumanKeyboard.type_text(page, selector, value, clear_first=True)
        HumanTiming.between_actions()
        field = "(sensitive)" if sensitive else selector
        _capture_and_queue_frame(page)
        _record_macro_step("fill", selector=selector, value=value if not sensitive else "***", sensitive=sensitive)
        _update_browser_conv_state("fill", selector=selector, value=value, sensitive=sensitive)
        return f"Filled {field}, length={len(value)}"
    except Exception as e:
        return f"Error filling {selector}: {e}"


def browser_scroll(
    direction: str = "down",
    amount: str | int = "medium",
    selector: str | None = None,
) -> str:
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    try:
        if selector and str(selector).strip():
            try:
                page.locator(selector).first.scroll_into_view_if_needed(timeout=8000)
            except Exception:
                pass
        distances = {
            "small": (100, 250),
            "medium": (250, 500),
            "large": (500, 900),
            "page": (800, 1200),
        }
        if isinstance(amount, int):
            distance = amount
        else:
            lo, hi = distances.get(str(amount), (250, 500))
            distance = random.randint(lo, hi)
        HumanKeyboard.scroll_naturally(page, direction, distance)
        HumanTiming.think(300, 700)
        return f"Scrolled {direction} ~{distance}px"
    except Exception as e:
        return f"Error browser_scroll: {e}"


def browser_wait_for_human(condition: str, timeout_ms: int = 10000) -> str:
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    try:
        if condition == "network_idle":
            page.wait_for_load_state("networkidle", timeout=timeout_ms)
        elif condition == "navigation":
            page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
        else:
            deadline = time.monotonic() + timeout_ms / 1000.0
            while time.monotonic() < deadline:
                try:
                    page.wait_for_selector(condition, timeout=1000)
                    break
                except Exception:
                    time.sleep(random.uniform(0.3, 0.8))
            else:
                return f"Error: timeout waiting for selector {condition}"
        HumanTiming.after_navigate()
        return f"Waited for: {condition}"
    except Exception as e:
        return f"Error browser_wait_for_human: {e}"


def screenshot_browser(path: str = "/tmp/browser.png") -> str:
    try:
        _get_page().screenshot(path=path)
    except BrowserCDPError as e:
        return f"Error: {e}"
    return path


def evaluate(js: str) -> str:
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    try:
        result = page.evaluate(js)
        return str(result)[:3000]
    except Exception as e:
        return f"Error: {e}"


def get_dom_state() -> str:
    """
    Snapshot nhanh trạng thái DOM hiện tại — không cần vision API.
    Trả về JSON với: url, title, readyState, visible inputs/buttons/links, scroll position, alerts.
    Dùng để Claude hiểu trang đang ở đâu mà không tốn vision call.
    """
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    try:
        js = """
        (() => {
            const inputs = Array.from(document.querySelectorAll('input:not([type=hidden]),textarea,select'))
                .filter(el => {
                    const r = el.getBoundingClientRect();
                    return r.width > 0 && r.height > 0;
                })
                .slice(0, 15)
                .map(el => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.type || '',
                    name: el.name || el.id || el.placeholder || '',
                    value: el.type === 'password' ? '***' : (el.value || '').slice(0, 80),
                    required: el.required || false
                }));

            const buttons = Array.from(document.querySelectorAll('button,input[type=submit],[role=button]'))
                .filter(el => {
                    const r = el.getBoundingClientRect();
                    return r.width > 0 && r.height > 0;
                })
                .slice(0, 10)
                .map(el => ({
                    text: (el.innerText || el.value || el.ariaLabel || '').trim().slice(0, 60),
                    disabled: el.disabled || false
                }));

            const links = Array.from(document.querySelectorAll('a[href]'))
                .filter(el => {
                    const r = el.getBoundingClientRect();
                    return r.width > 0 && r.height > 0;
                })
                .slice(0, 10)
                .map(el => ({
                    text: (el.innerText || '').trim().slice(0, 60),
                    href: el.href.slice(0, 120)
                }));

            const alerts = Array.from(document.querySelectorAll(
                '[role=alert],[role=status],.alert,.notification,.toast,.error-message,.success-message'
            )).slice(0, 5).map(el => (el.innerText || '').trim().slice(0, 150));

            const modal = !!document.querySelector('[role="dialog"],[role="alertdialog"],.modal.show');

            return {
                url: location.href,
                title: document.title,
                readyState: document.readyState,
                scrollY: Math.round(window.scrollY),
                pageHeight: Math.round(document.body ? document.body.scrollHeight : 0),
                modal,
                inputs,
                buttons,
                links,
                alerts
            };
        })()
        """
        import json as _json
        result = page.evaluate(js)
        return _json.dumps(result, ensure_ascii=False, indent=2)[:4000]
    except Exception as e:
        return f"Error get_dom_state: {e}"


def browser_run_sequence(actions: list) -> str:
    """
    Chạy danh sách actions tuần tự trong một lần gọi — tiết kiệm nhiều LLM round-trips.
    Mỗi action là dict {"action": str, ...params}.
    Actions: navigate, click, fill, scroll, wait, wait_dom_stable, get_dom_state, evaluate, screenshot.
    Trả về JSON list kết quả từng bước.
    """
    import json as _json
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    results = []
    for i, act in enumerate(actions):
        atype = (act.get("action") or "").strip().lower()
        step_label = f"step{i+1}:{atype}"
        try:
            if atype == "navigate":
                r = navigate(act["url"], act.get("wait_for", "load"))
            elif atype == "click":
                r = click_selector(act.get("selector"), act.get("text"))
            elif atype == "fill":
                r = fill(act["selector"], act["value"], bool(act.get("sensitive", False)))
            elif atype == "scroll":
                r = browser_scroll(act.get("direction", "down"), act.get("amount", "medium"), act.get("selector"))
            elif atype == "wait":
                ms = int(act.get("ms", 500))
                time.sleep(ms / 1000.0)
                r = f"Waited {ms}ms"
            elif atype == "wait_dom_stable":
                _wait_for_dom_stable(page, int(act.get("timeout_ms", 1000)))
                r = "DOM stable"
            elif atype == "get_dom_state":
                r = get_dom_state()
            elif atype == "evaluate":
                r = evaluate(act["js"])
            elif atype == "screenshot":
                _capture_and_queue_frame(page)
                r = "Screenshot queued"
            elif atype == "fill_form":
                r = browser_fill_form(act.get("data", {}))
            else:
                r = f"Error: unknown action '{atype}'"
            results.append({"step": step_label, "ok": not str(r).startswith("Error"), "result": str(r)[:400]})
            if str(r).startswith("Error"):
                results.append({"step": "aborted", "ok": False, "result": f"Dừng tại {step_label}"})
                break
        except Exception as e:
            results.append({"step": step_label, "ok": False, "result": f"Exception: {e}"})
            break
    return _json.dumps(results, ensure_ascii=False, indent=2)


def browser_fill_form(data: dict) -> str:
    """
    Tự động điền form bằng fuzzy-match: khớp key của data với name/id/placeholder/aria-label.
    data = {"email": "...", "password": "...", "username": "..."}
    Không cần biết CSS selector chính xác.
    """
    import json as _json
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    if not data:
        return "Error: data rỗng"
    filled = []
    failed = []
    for key, value in data.items():
        key_lower = key.lower().strip()
        # Thử các locator strategies theo độ ưu tiên
        locators_to_try = [
            page.locator(f"[name='{key}']"),
            page.locator(f"[id='{key}']"),
            page.locator(f"[name*='{key_lower}' i]"),
            page.locator(f"[id*='{key_lower}' i]"),
            page.locator(f"[placeholder*='{key_lower}' i]"),
            page.locator(f"[aria-label*='{key_lower}' i]"),
            page.locator(f"[data-testid*='{key_lower}' i]"),
            page.locator(f"label:has-text('{key_lower}') + input"),
            page.locator(f"label:has-text('{key_lower}') ~ input"),
        ]
        filled_this = False
        for loc in locators_to_try:
            try:
                if _locator_ready(loc, 500):
                    el = loc.first
                    el.scroll_into_view_if_needed(timeout=3000)
                    sensitive = key_lower in ("password", "passwd", "pass", "pwd", "secret", "token")
                    if sensitive:
                        el.click(timeout=5000)
                        # Clear field trước khi gõ (tránh append vào text có sẵn)
                        try:
                            el.fill("", timeout=2000)
                            if el.input_value() != "":
                                # Fallback: select-all + delete
                                import platform as _p
                                mod = "Meta" if _p.system() == "Darwin" else "Control"
                                page.keyboard.press(f"{mod}+A")
                                page.keyboard.press("Backspace")
                        except Exception:
                            pass
                        page.keyboard.type(str(value), delay=random.uniform(40, 80))
                    else:
                        el.fill(str(value))
                    filled.append(key)
                    filled_this = True
                    break
            except Exception:
                continue
        if not filled_this:
            failed.append(key)
    HumanTiming.between_actions()
    _capture_and_queue_frame(page)
    msg = f"Đã fill: {filled}"
    if failed:
        msg += f" | Không tìm thấy: {failed}"
    return msg


def browser_set_resource_blocking(
    block: list | None = None,
    unblock: list | None = None,
    clear: bool = False,
) -> str:
    """
    Bật/tắt block loại tài nguyên để tăng tốc load trang.
    block: list resource types cần block, ví dụ ["image","font","media","stylesheet"]
    unblock: list resource types cần bỏ block
    clear: True = tắt toàn bộ blocking
    Resource types: document, stylesheet, image, media, font, script, texttrack,
                    xhr, fetch, eventsource, websocket, manifest, other
    """
    global _blocked_resource_types, _resource_blocking_active
    if clear:
        _blocked_resource_types = set()
        _resource_blocking_active = False
        return "Đã tắt resource blocking"
    if block:
        _blocked_resource_types.update(block)
        _resource_blocking_active = True
    if unblock:
        _blocked_resource_types -= set(unblock)
        if not _blocked_resource_types:
            _resource_blocking_active = False
    if _resource_blocking_active and _current_page:
        _apply_resource_blocking(_current_page)
    status = f"Đang block: {sorted(_blocked_resource_types)}" if _resource_blocking_active else "Resource blocking: tắt"
    return status


def get_page_state() -> str:
    """
    Page State Machine — trả về state hiện tại của trang dựa trên URL change + DOM.
    States: LOADING, READY, FORM_VISIBLE, SUBMITTED, SUCCESS, ERROR, AUTH_REQUIRED, CAPTCHA.
    Nhanh hơn intent gate — dùng thuần heuristics, không gọi vision API.
    """
    import json as _json
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    try:
        js = """
        (() => {
            const url = location.href;
            const text = (document.body?.innerText || '').toLowerCase().slice(0, 3000);
            const title = document.title.toLowerCase();
            const readyState = document.readyState;

            // Loading check
            const spinners = document.querySelectorAll(
                '.loading,.spinner,[data-loading],#loading,[aria-busy=true]'
            );
            const hasSpinner = [...spinners].some(el => {
                const r = el.getBoundingClientRect();
                return r.width > 0 && r.height > 0;
            });
            if (readyState !== 'complete' || hasSpinner) return 'LOADING';

            // Auth / login
            const hasLoginForm = !!(
                document.querySelector('input[type=password]') &&
                document.querySelector('input[type=email], input[type=text][name*=user], input[name*=email], input[name*=login]')
            );
            if (hasLoginForm) return 'FORM_VISIBLE:login';

            // Captcha
            if (text.includes('captcha') || text.includes('recaptcha') || text.includes('hcaptcha') ||
                !!document.querySelector('[class*=captcha],[id*=captcha],.cf-challenge')) return 'CAPTCHA';

            // Error state
            const hasError = !!(
                document.querySelector('[role=alert].error, .error-message, .alert-danger') ||
                text.match(/error|lỗi|failed|thất bại|không thành công/) &&
                !text.match(/no error|no lỗi/)
            );
            if (hasError) return 'ERROR';

            // Success state
            const hasSuccess = !!(
                document.querySelector('.success, .alert-success, [role=alert].success') ||
                text.match(/thành công|success|done|complete|đã lưu|đã gửi|cảm ơn|thank you/)
            );
            if (hasSuccess) return 'SUCCESS';

            // General form visible
            const visibleForms = [...document.querySelectorAll('form,input:not([type=hidden])')].filter(el => {
                const r = el.getBoundingClientRect();
                return r.width > 0 && r.height > 0;
            });
            if (visibleForms.length > 0) return 'FORM_VISIBLE';

            return 'READY';
        })()
        """
        state = page.evaluate(js)
        url = ""
        try:
            url = page.url or ""
        except Exception:
            pass
        return _json.dumps({"state": state, "url": url, "title": ""}, ensure_ascii=False)
    except Exception as e:
        return f"Error get_page_state: {e}"


def launch_human_browser():
    """
    Entry tương đương spec «launch_human_browser»: khởi tạo Chrome (CDP hoặc persistent)
    với anti-detection init scripts + human behavior trong các tool navigate/click/fill.
    """
    return _get_page()


def browser_batch_fetch(urls: list, extract_js: str = "document.title") -> str:
    """
    Fetch nhiều URL tuần tự — mỗi URL mở tab mới, chạy extract_js, đóng tab.
    Playwright sync API không cho phép gọi song song trên cùng 1 context, nên phải tuần tự.
    Dùng khi cần quét nhanh nhiều URL mà không tạo nhiều page riêng biệt.
    Trả về JSON {url: result} cho mọi URL.
    Ví dụ: browser_batch_fetch(["url1","url2"], "document.body.innerText.slice(0,500)")
    """
    import json as _json
    try:
        context = _context
        if context is None:
            _get_page()
            context = _context
        if context is None:
            return "Error: Browser chưa khởi tạo"
    except Exception as e:
        return f"Error: {e}"

    def _fetch_one(url: str) -> tuple[str, str]:
        pg = None
        try:
            pg = context.new_page()
            pg.goto(url, wait_until="domcontentloaded", timeout=15000)
            smart_wait(pg)
            result = pg.evaluate(extract_js)
            return url, str(result)[:1000]
        except Exception as exc:
            return url, f"Error: {exc}"
        finally:
            if pg:
                try:
                    pg.close()
                except Exception:
                    pass

    results = {}
    for u in urls:
        url, res = _fetch_one(u)
        results[url] = res

    return _json.dumps(results, ensure_ascii=False, indent=2)


# Backward-compat alias — tên cũ gây hiểu nhầm là "song song"
browser_parallel_fetch = browser_batch_fetch


def set_browser_conv_id(conv_id: str) -> None:
    """Gán conversation ID hiện tại để track browser context per conversation."""
    global _current_conv_id
    _current_conv_id = conv_id


def get_browser_conv_context(conv_id: str = "") -> dict:
    """Lấy browser context state của một conversation."""
    cid = conv_id or _current_conv_id
    return _browser_conv_state.get(cid, {})


def _update_browser_conv_state(action: str, **kwargs) -> None:
    """Cập nhật conversation state sau mỗi action."""
    cid = _current_conv_id
    if not cid:
        return
    state = _browser_conv_state.setdefault(cid, {
        "url": "", "visited": [], "fills": {}, "ts": time.time()
    })
    state["ts"] = time.time()
    if action == "navigate":
        url = kwargs.get("url", "")
        state["url"] = url
        if url and url not in state["visited"]:
            state["visited"].append(url)
            if len(state["visited"]) > 30:
                state["visited"] = state["visited"][-30:]
    elif action == "fill":
        sel = kwargs.get("selector", "")
        val = kwargs.get("value", "")
        if sel and not kwargs.get("sensitive", False):
            state["fills"][sel] = str(val)[:100]
    # Giữ tối đa 50 conversations
    if len(_browser_conv_state) > 50:
        oldest = min(_browser_conv_state, key=lambda k: _browser_conv_state[k].get("ts", 0))
        _browser_conv_state.pop(oldest, None)


def browser_get_conv_context() -> str:
    """
    Trả về browser context của conversation hiện tại:
    URL hiện tại, các URL đã visit, các field đã fill trong session.
    Giúp Claude biết context mà không cần re-navigate.
    """
    import json as _json
    ctx = get_browser_conv_context()
    if not ctx:
        return '{"status": "Chưa có browser context cho conversation này"}'
    return _json.dumps(ctx, ensure_ascii=False, indent=2)


def _screenshot_on_error(page, context_label: str = "") -> str:
    """
    Chụp screenshot nhỏ (JPEG 50%) khi gặp lỗi, trả về base64 để đính kèm error message.
    """
    try:
        png = page.screenshot(type="jpeg", quality=50, timeout=3000)
        b64 = base64.standard_b64encode(png).decode()
        _BROWSER_FRAME_QUEUE.append({
            "type": "browser_frame",
            "base64": b64,
            "url": "",
            "label": f"error_screenshot:{context_label}",
        })
        return f"[Screenshot on error đã queue — xem browser preview]"
    except Exception:
        return ""


def browser_macro_record(name: str) -> str:
    """Bắt đầu ghi macro với tên cho trước. Mọi navigate/click/fill sau đó sẽ được record."""
    global _macro_recording, _macro_steps
    _macro_recording = True
    _macro_steps = []
    return f"Bắt đầu ghi macro '{name}'"


def browser_macro_stop(name: str) -> str:
    """Dừng ghi macro và lưu vào library với key là tên site/task."""
    global _macro_recording, _macro_steps, _macro_library
    import json as _json
    _macro_recording = False
    if not _macro_steps:
        return "Macro rỗng — không lưu"
    key = name.strip().lower().replace(" ", "_")
    _macro_library[key] = list(_macro_steps)
    _macro_steps = []
    return f"Đã lưu macro '{key}' ({len(_macro_library[key])} bước): {_json.dumps(_macro_library[key], ensure_ascii=False)[:300]}"


def browser_macro_replay(name: str, timing_variance: float = 0.2) -> str:
    """
    Replay macro đã ghi theo tên. Thực thi các bước đã record.
    timing_variance: 0.0-0.5 — độ biến đổi ngẫu nhiên ±% cho mọi delay (tránh pattern nhận dạng).
    Tiết kiệm toàn bộ LLM round-trips cho task lặp lại.
    """
    key = name.strip().lower().replace(" ", "_")
    steps = _macro_library.get(key)
    if not steps:
        available = list(_macro_library.keys())
        return f"Error: Không tìm thấy macro '{key}'. Có sẵn: {available}"
    # Apply timing variance: jitter explicit wait steps so each replay looks different
    tv = max(0.0, min(0.5, timing_variance))
    varied_steps = []
    for step in steps:
        s = dict(step)
        if s.get("action") == "wait" and "ms" in s:
            ms = int(s["ms"])
            jitter = ms * random.uniform(-tv, tv)
            s["ms"] = max(50, int(ms + jitter))
        varied_steps.append(s)
    # Also add small random inter-step pauses to vary overall rhythm
    sequenced = []
    for s in varied_steps:
        sequenced.append(s)
        if tv > 0 and s.get("action") not in ("wait",):
            jitter_ms = int(random.uniform(80, 250) * tv)
            if jitter_ms > 30:
                sequenced.append({"action": "wait", "ms": jitter_ms})
    return browser_run_sequence(sequenced)


def browser_macro_list() -> str:
    """Liệt kê tất cả macros đã lưu."""
    import json as _json
    if not _macro_library:
        return "Chưa có macro nào được lưu"
    summary = {k: f"{len(v)} bước" for k, v in _macro_library.items()}
    return _json.dumps(summary, ensure_ascii=False, indent=2)


_VALID_MACRO_ACTIONS = {
    "navigate", "click", "fill", "scroll", "evaluate", "new_tab", "switch_tab",
    "close_tab", "screenshot", "wait", "keyboard_press",
}


def _locator_ready(loc, timeout_ms: int = 800) -> bool:
    """Chờ locator attach vào DOM rồi mới trả về True.
    Thay thế pattern `loc.count() > 0` (race khi DOM còn đang render)."""
    try:
        loc.first.wait_for(state="attached", timeout=timeout_ms)
        return True
    except Exception:
        return False


def _iframe_locators(page, selector: str | None = None, text: str | None = None):
    """Trả về list locator trong tất cả iframe có thể pierce được.
    Thử frame_locator cho mỗi iframe hiển thị; bỏ qua cross-origin frame."""
    frame_locators = []
    try:
        frame_count = page.locator("iframe").count()
    except Exception:
        return frame_locators
    for i in range(min(frame_count, 8)):
        try:
            fl = page.frame_locator(f"iframe >> nth={i}")
            if selector:
                frame_locators.append((f"iframe[{i}] {selector}", fl.locator(selector)))
            if text:
                frame_locators.append((f"iframe[{i}] text={text!r}", fl.get_by_text(text, exact=False)))
        except Exception:
            continue
    return frame_locators


def _record_macro_step(action: str, **kwargs) -> None:
    """Ghi bước vào macro nếu đang recording. Validate action name để bắt typo sớm."""
    if not _macro_recording:
        return
    if action not in _VALID_MACRO_ACTIONS:
        # Cảnh báo nhưng vẫn ghi để không chặn flow — dev sẽ thấy trong log
        print(f"[Browser macro] Cảnh báo: action '{action}' không có trong whitelist {sorted(_VALID_MACRO_ACTIONS)}")
    step = {"action": action}
    step.update({k: v for k, v in kwargs.items() if v is not None})
    _macro_steps.append(step)


def browser_verify_action(
    expected: str,
    timeout_ms: int = 3000,
) -> str:
    """
    DOM diff verify sau action — không cần screenshot.
    expected: "url_changed" | "form_disappeared" | "alert_appeared" | "success" | "error" | "any_change"
    Nhanh hơn vision: thuần JS so sánh DOM state trước/sau.
    """
    import json as _json
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    try:
        before_js = """(() => ({
            url: location.href,
            hasForm: !!document.querySelector('form input:not([type=hidden])'),
            alerts: [...document.querySelectorAll('[role=alert],.alert,.toast')].map(el => el.innerText.trim().slice(0,80)),
            hasSuccess: !!document.querySelector('.success,.alert-success,[class*=success]'),
            hasError: !!document.querySelector('.error,.alert-danger,[class*=error],[role=alert]'),
        }))()"""
        before = page.evaluate(before_js)
        time.sleep(timeout_ms / 1000.0)
        after = page.evaluate(before_js)

        results = {}
        url_changed = before["url"] != after["url"]
        form_disappeared = before["hasForm"] and not after["hasForm"]
        alert_appeared = len(after["alerts"]) > len(before["alerts"])
        has_success = after["hasSuccess"]
        has_error = after["hasError"]

        expected_lower = expected.lower()
        if expected_lower == "url_changed":
            ok = url_changed
        elif expected_lower == "form_disappeared":
            ok = form_disappeared
        elif expected_lower == "alert_appeared":
            ok = alert_appeared
        elif expected_lower == "success":
            ok = has_success or url_changed or form_disappeared
        elif expected_lower == "error":
            ok = has_error
        else:  # any_change
            ok = url_changed or form_disappeared or alert_appeared or has_success or has_error

        results = {
            "verified": ok,
            "expected": expected,
            "url_changed": url_changed,
            "form_disappeared": form_disappeared,
            "alert_appeared": alert_appeared,
            "has_success": has_success,
            "has_error": has_error,
            "new_url": after["url"] if url_changed else None,
            "new_alerts": after["alerts"] if alert_appeared else [],
        }
        return _json.dumps(results, ensure_ascii=False)
    except Exception as e:
        return f"Error browser_verify_action: {e}"


def browser_preflight_check(url: str) -> str:
    """
    Kiểm tra nhanh một URL trước khi navigate:
    - Dùng curl HEAD để check HTTP status, Cloudflare headers, redirect chain
    - Cảnh báo sớm nếu có bot detection, rate limit, redirect đáng ngờ
    - Không tốn Playwright page load
    """
    import json as _json
    import subprocess as _sp
    try:
        result = _sp.run(
            ["curl", "-s", "-I", "-L", "--max-time", "5", "--max-redirs", "3",
             "-A", DEFAULT_USER_AGENT, url],
            capture_output=True, text=True, timeout=8
        )
        headers_raw = result.stdout.lower()
        warnings = []

        # Cloudflare bot detection
        if "cf-ray:" in headers_raw or "cloudflare" in headers_raw:
            if "403" in headers_raw or "challenge" in headers_raw:
                warnings.append("CLOUDFLARE_BLOCK: Trang dùng Cloudflare challenge — có thể cần browser thật")
            else:
                warnings.append("CLOUDFLARE: Trang dùng Cloudflare CDN")

        # HTTP status
        status_match = None
        for line in result.stdout.split("\n"):
            if line.startswith("HTTP/"):
                status_match = line.strip()
        if status_match:
            if "403" in status_match:
                warnings.append(f"HTTP 403 Forbidden — trang từ chối request")
            elif "429" in status_match:
                warnings.append(f"HTTP 429 Too Many Requests — đang bị rate limit")
            elif "503" in status_match:
                warnings.append(f"HTTP 503 Service Unavailable")
            elif "301" in status_match or "302" in status_match:
                warnings.append(f"Redirect: {status_match}")

        # Bot detection headers
        for h in ["x-robots-tag: noindex", "x-frame-options:", "content-security-policy:"]:
            if h in headers_raw:
                pass  # normal

        output = {
            "url": url,
            "status": status_match or "unknown",
            "warnings": warnings,
            "safe_to_navigate": len([w for w in warnings if "BLOCK" in w or "403" in w or "429" in w]) == 0,
        }
        return _json.dumps(output, ensure_ascii=False, indent=2)
    except Exception as e:
        return _json.dumps({"url": url, "status": "check_failed", "error": str(e), "safe_to_navigate": True}, ensure_ascii=False)


def browser_set_network_throttle(profile: str = "wifi") -> str:
    """
    Mô phỏng điều kiện mạng thực tế qua CDP Network.emulateNetworkConditions.
    profile: "wifi" | "4g" | "3g" | "slow_3g" | "offline" | "off"
    Giúp timing thao tác phù hợp với trải nghiệm người dùng thực.
    """
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    profiles = {
        "wifi":     {"downloadThroughput": 10_000_000 / 8, "uploadThroughput": 5_000_000 / 8, "latency": 20},
        "4g":       {"downloadThroughput": 4_000_000 / 8,  "uploadThroughput": 3_000_000 / 8,  "latency": 50},
        "3g":       {"downloadThroughput": 1_500_000 / 8,  "uploadThroughput": 750_000 / 8,    "latency": 100},
        "slow_3g":  {"downloadThroughput": 400_000 / 8,    "uploadThroughput": 300_000 / 8,    "latency": 400},
        "offline":  {"downloadThroughput": 0, "uploadThroughput": 0, "latency": 0},
    }
    if profile == "off":
        cdp = None
        try:
            cdp = page.context.new_cdp_session(page)
            cdp.send("Network.emulateNetworkConditions", {
                "offline": False, "downloadThroughput": -1, "uploadThroughput": -1, "latency": 0
            })
            return "Network throttle: tắt (mạng thật)"
        except Exception as e:
            return f"Error removing throttle: {e}"
        finally:
            if cdp is not None:
                try: cdp.detach()
                except Exception: pass
    cfg = profiles.get(profile.lower())
    if not cfg:
        return f"Error: profile không hợp lệ. Chọn: {list(profiles.keys()) + ['off']}"
    cdp = None
    try:
        cdp = page.context.new_cdp_session(page)
        cdp.send("Network.emulateNetworkConditions", {
            "offline": profile == "offline",
            **cfg,
            "connectionType": "wifi" if profile == "wifi" else "cellular4g" if profile == "4g" else "cellular3g",
        })
        return f"Network throttle: {profile} ({cfg['latency']}ms latency, ↓{cfg['downloadThroughput']*8/1_000_000:.1f}Mbps)"
    except Exception as e:
        return f"Error setting throttle: {e}"
    finally:
        if cdp is not None:
            try: cdp.detach()
            except Exception: pass


def browser_wait_for_stable(selector: str, timeout_ms: int = 5000) -> str:
    """
    Đợi element xuất hiện, visible, và trang không còn spinner/loading state.
    Thông minh hơn page.wait_for_selector — kiểm tra cả DOM stability.
    """
    try:
        page = _get_page()
    except BrowserCDPError as e:
        return f"Error: {e}"
    try:
        loc = page.locator(selector)
        loc.wait_for(state="visible", timeout=timeout_ms)
        # Wait for spinners/loaders to disappear
        for spinner_sel in [".loading", ".spinner", "[aria-busy='true']", "#loading", "[data-loading]"]:
            try:
                page.wait_for_selector(spinner_sel, state="hidden", timeout=min(1500, timeout_ms // 3))
            except Exception:
                pass
        # Wait for DOM to stop mutating (SPA hydration settle)
        _wait_for_dom_stable(page, min(800, timeout_ms // 4))
        box = None
        try:
            box = loc.first.bounding_box()
        except Exception:
            pass
        if box:
            return f"Element stable: selector={selector!r} at ({int(box['x'])},{int(box['y'])})"
        return f"Element visible: selector={selector!r}"
    except Exception as e:
        return f"Error browser_wait_for_stable: {e}"


def close_browser():
    """Đóng browser và giải phóng resources."""
    global _pw, _context, _current_page, _pages, _playwright_persistent_launched
    global _init_scripts_applied_to
    _watchdog_stop.set()
    try:
        if _context:
            try:
                save_browser_session(_context)
            except Exception:
                pass
            _context.close()
        if _pw:
            _pw.stop()
    except Exception:
        pass
    _pw = None
    _context = None
    _current_page = None
    _pages = []
    _playwright_persistent_launched = False
    _init_scripts_applied_to = None
