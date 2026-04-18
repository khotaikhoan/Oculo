"""
Oculo Web Server — upgraded with streaming, retry, context injection,
structured output, memory consolidation, task decomposition, self-correction,
preference learning, tool parallelism, response caching, model routing, prompt compression,
multi-tab browser, tool summarization, error recovery, checkpoints, API key rotation,
sensitive data masking, conversation title generation.
"""
import collections, os, json, base64, threading, time, traceback, uuid, shutil, subprocess
from datetime import datetime
from urllib import request as urlrequest
from urllib import error as urlerror
from apscheduler.schedulers.background import BackgroundScheduler
import anthropic
from flask import Flask, request, jsonify, Response, send_from_directory
from dotenv import load_dotenv
from tools import desktop, browser
from tools.vision_dom import (
    browser_analyze_page_tool,
    browser_vision_click_tool,
    browser_vision_type_tool,
)
from memory import store as memory_store
from agents.orchestrator import run_pipeline
from proactive import monitor as proactive_monitor

from version import APP_NAME, APP_VERSION

from utils.tool_cache import is_cacheable, get_cached, set_cache
from utils.model_router import route_model, ModelRoutingDecision
from utils.prompt_compressor import compress_history
from utils.context_injector import get_environment_context
from utils.task_decomposer import decompose_task
from utils.self_corrector import verify_write_file, verify_browser_navigate
from utils.preference_tracker import (
    detect_preferences, load_preferences,
    save_preferences, build_preference_prompt,
)
from utils.tool_parallel import can_run_parallel, run_tools_parallel
from utils.cost_optimizer import (
    build_cached_system, should_use_tools,
    filter_memories, build_memory_context,
    should_verify_write, should_verify_navigate,
    TokenUsageTracker,
)
from utils.tool_summarizer import maybe_summarize
from utils.checkpoint import save_checkpoint, list_checkpoints, restore_checkpoint
from utils.error_classifier import ErrorClassifier, ErrorCategory
from utils.retry_engine import run_with_retry
from utils.fallback_registry import execute_fallback
from utils.task_progress import progress_store, create_task, record_step
from utils.api_key_manager import key_manager
from utils.data_masker import mask_with_flag
from utils.model_display import model_ui_meta, model_ui_meta_openai_compat, enrich_models_list
from utils.openai_compat import (
    openai_compat_configured,
    list_openai_compat_model_ids,
    is_openai_compat_model,
)
from utils.openai_bridge import (
    anthropic_tools_to_openai,
    anthropic_messages_to_openai,
    flatten_cached_system,
    build_openai_response_like_anthropic,
    usage_from_openai,
)

from utils.app_paths import resource_dir as _resource_dir, dotenv_path as _dotenv_path

load_dotenv(_dotenv_path())

# Dùng đường dẫn tuyệt đối tới static/ — khi chạy trong .app (PyInstaller)
# thư mục hiện tại là "/" và static_folder relative sẽ không tìm thấy file.
_STATIC_DIR = str(_resource_dir() / "static")

app = Flask(__name__, static_folder=_STATIC_DIR)


def _tool_use_id_str(tid) -> str:
    return str(tid) if tid is not None else ""


# ── Image resize — giảm token cost cho ảnh đính kèm ──
_IMAGE_MAX_PX = int(os.getenv("IMAGE_MAX_PX", "1024"))

def _resize_image_b64(b64_data: str, mime: str) -> str:
    """
    Resize ảnh xuống max _IMAGE_MAX_PX px (giữ aspect ratio).
    Trả về b64 gốc nếu PIL không có hoặc ảnh đã nhỏ.
    """
    try:
        from PIL import Image as _PILImage
        import io as _io
        raw = base64.b64decode(b64_data)
        img = _PILImage.open(_io.BytesIO(raw))
        w, h = img.size
        if max(w, h) <= _IMAGE_MAX_PX:
            return b64_data  # đã đủ nhỏ
        ratio = _IMAGE_MAX_PX / max(w, h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        img = img.resize((new_w, new_h), _PILImage.LANCZOS)
        buf = _io.BytesIO()
        fmt = "JPEG" if mime in ("image/jpeg", "image/jpg") else "PNG"
        img.save(buf, format=fmt, quality=85, optimize=True)
        return base64.standard_b64encode(buf.getvalue()).decode()
    except Exception:
        return b64_data  # fallback: giữ nguyên


# ── Trim tool results trong history để tiết kiệm context ──
_TOOL_RESULT_TRIM = int(os.getenv("TOOL_RESULT_TRIM_CHARS", "600"))

def _trim_history_tool_results(messages: list) -> list:
    """
    Rút gọn tool_result content trong history xuống _TOOL_RESULT_TRIM chars.
    Giữ nguyên message cuối (user hiện tại) để không mất thông tin.
    """
    if not messages or _TOOL_RESULT_TRIM <= 0:
        return messages
    trimmed = []
    for i, msg in enumerate(messages):
        # Bỏ qua message cuối — đó là user message hiện tại
        if i == len(messages) - 1:
            trimmed.append(msg)
            continue
        content = msg.get("content")
        if not isinstance(content, list):
            trimmed.append(msg)
            continue
        new_content = []
        changed = False
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_result":
                raw = block.get("content", "")
                if isinstance(raw, str) and len(raw) > _TOOL_RESULT_TRIM:
                    block = {**block, "content": raw[:_TOOL_RESULT_TRIM] + f"\n…[trimmed {len(raw)-_TOOL_RESULT_TRIM} chars]"}
                    changed = True
            new_content.append(block)
        trimmed.append({**msg, "content": new_content} if changed else msg)
    return trimmed


def _is_error_result_text(s) -> bool:
    t = ("" if s is None else str(s)).strip()
    if not t:
        return False
    tl = t.lower()
    return t.startswith("Error:") or t.startswith("Lỗi:") or tl.startswith("error:") or tl.startswith("lỗi:")


def _extract_text_from_content(content_blocks, default: str = "") -> str:
    """Safely extract first text block from Anthropic API content list."""
    if not content_blocks:
        return default
    for block in content_blocks:
        if hasattr(block, "type") and block.type == "text":
            return block.text
        if isinstance(block, dict) and block.get("type") == "text":
            return block.get("text", default)
    return default


def _tool_result_payload(name, raw_for_err, masked_full, was_masked, tool_use_id, **extra):
    mt = masked_full if isinstance(masked_full, str) else str(masked_full)
    d = {
        "type": "tool_result",
        "name": name,
        "result": mt[:800],
        "masked": was_masked,
        "tool_use_id": _tool_use_id_str(tool_use_id),
        "is_error": _is_error_result_text(raw_for_err),
        **extra,
    }
    return d

# ── Simple rate limiting ──
_rate_limit_store: dict[str, collections.deque] = {}
_rate_limit_lock = threading.Lock()
_RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "30"))   # requests
_RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
_RATE_LIMIT_MAX_IPS = 10000  # tránh phình dict vô hạn

def _check_rate_limit(client_ip: str) -> bool:
    """Returns True if request is allowed, False if rate limited."""
    now = time.time()
    with _rate_limit_lock:
        if client_ip not in _rate_limit_store:
            if len(_rate_limit_store) >= _RATE_LIMIT_MAX_IPS:
                oldest = next(iter(_rate_limit_store))
                del _rate_limit_store[oldest]
            _rate_limit_store[client_ip] = collections.deque()
        dq = _rate_limit_store[client_ip]
        while dq and dq[0] < now - _RATE_LIMIT_WINDOW:
            dq.popleft()
        if len(dq) >= _RATE_LIMIT_MAX:
            return False
        dq.append(now)
        # Xóa key khi không còn request để tiết kiệm bộ nhớ
        if not dq:
            del _rate_limit_store[client_ip]
        return True

# ── Env context cache (30s TTL) ──
_env_ctx_cache: dict = {"value": "", "ts": 0.0}
_ENV_CTX_TTL = 30  # seconds

def _get_env_context_cached() -> str:
    now = time.time()
    if now - _env_ctx_cache["ts"] < _ENV_CTX_TTL:
        return _env_ctx_cache["value"]
    ctx = get_environment_context()
    _env_ctx_cache["value"] = ctx
    _env_ctx_cache["ts"] = now
    return ctx


# Patterns cho thấy user cần biết về môi trường hệ thống
_ENV_CONTEXT_PATTERNS = [
    "màn hình", "screen", "desktop", "ứng dụng", "app", "mở", "open",
    "cpu", "ram", "disk", "memory", "process", "terminal", "thư mục",
    "folder", "file", "pwd", "path", "đường dẫn", "hệ thống", "system",
    "chụp", "screenshot", "cửa sổ", "window", "finder", "safari", "chrome",
]

def _should_inject_env_context(query: str) -> bool:
    """Chỉ inject env context khi query liên quan đến hệ thống/UI."""
    q = query.lower()
    return any(p in q for p in _ENV_CONTEXT_PATTERNS)


def _get_query_text(user_content) -> str:
    """
    Tách ngữ nghĩa để dùng cho router/memory:
    - Nếu user_content là string: dùng trực tiếp.
    - Nếu user_content là list (text + image blocks): chỉ lấy block type='text' (tránh lôi base64).
    - Nếu không có text nhưng có ảnh: dùng placeholder.
    """
    if isinstance(user_content, str):
        return user_content[:200]
    if isinstance(user_content, list):
        texts: list[str] = []
        has_images = False
        for b in user_content:
            if not isinstance(b, dict):
                continue
            t = b.get("type")
            if t == "text":
                v = b.get("text", "")
                if isinstance(v, str) and v.strip():
                    texts.append(v.strip())
            elif t == "image":
                has_images = True
        joined = "\n".join(texts).strip()
        if not joined and has_images:
            joined = "[Đã đính kèm ảnh]"
        return joined[:200]
    try:
        return str(user_content)[:200]
    except Exception:
        return ""


_client_pool: dict[str, anthropic.Anthropic] = {}

def get_client() -> anthropic.Anthropic:
    """Tái sử dụng client theo API key — tránh tạo httpx session mới mỗi request."""
    key = key_manager.get_key()
    if key not in _client_pool:
        _client_pool[key] = anthropic.Anthropic(
            api_key=key,
            base_url=os.getenv("ANTHROPIC_BASE_URL") or None,
        )
    return _client_pool[key]


def get_optional_anthropic_direct():
    """Computer Use / tính năng chỉ có trên Anthropic Messages API (beta). Không qua 9Router."""
    k = os.getenv("ANTHROPIC_API_KEY")
    if not k:
        return None
    return anthropic.Anthropic(api_key=k, base_url=os.getenv("ANTHROPIC_BASE_URL") or None)


client = get_client()

_OLLAMA_BASE_URL = (os.getenv("OLLAMA_BASE_URL") or "http://127.0.0.1:11434").rstrip("/")
_ollama_service_proc: subprocess.Popen | None = None
_ollama_models_cache: dict[str, object] = {"ts": 0.0, "items": []}
_ollama_spawn_lock = threading.Lock()
_OLLAMA_MODELS_TTL = 15.0

# ── Preferences in-memory cache (5 min TTL) ──
_prefs_cache: dict = {"obj": None, "prompt": "", "ts": 0.0}
_PREFS_CACHE_TTL = 300  # seconds

scheduler = BackgroundScheduler()
scheduler.start()
scheduled_jobs = {}
active_streams = {}

DEFAULT_MODEL  = os.getenv("MODEL", "claude-sonnet-4-5")
DEFAULT_TEMP   = 1.0

BROWSER_BEHAVIOR_PROMPT = """
Khi thực hiện task trên Chrome, hành xử như người thật:

NGUYÊN TẮC CHUNG:
- Luôn navigate đến trang trước khi tương tác — không assume trang đã mở
- Sau mỗi navigate: dùng screenshot_and_analyze để "nhìn" trang trước khi action
- Không click ngay — đọc layout trang, xác định đúng element
- Nếu không thấy element: scroll xuống trước khi kết luận "không có"
- Sau form submit: đợi và verify kết quả — không assume thành công

THỨ TỰ THỰC HIỆN CHUẨN:
1. browser_navigate(url)
2. screenshot_and_analyze → hiểu layout
3. browser_scroll nếu cần tìm element
4. browser_click / browser_fill
5. browser_wait_for_human(condition) nếu có loading
6. screenshot_and_analyze → verify kết quả

KHÔNG BAO GIỜ:
- Click/fill ngay sau navigate không có screenshot
- Chạy nhiều action liên tiếp không verify
- Dùng JavaScript inject để bypass UI — luôn tương tác qua UI thật

KHI GẶP CAPTCHA hoặc BLOCK:
- Dừng lại, báo cáo cho user ngay
- Không cố bypass tự động
"""

BROWSER_VISION_STRATEGY_PROMPT = """
CHIẾN LƯỢC BROWSER — DOM TRƯỚC, VISION SAU (quan trọng: vision rất chậm và tốn tiền):

Ưu tiên 1 — LUÔN thử DOM tools trước (nhanh, rẻ, không cần API vision):
- browser_get_dom_state: snapshot nhanh trang (URL, inputs, buttons, links, alerts, modal) — gọi ngay sau navigate để "nhìn" trang mà không tốn vision
- browser_evaluate: đọc text, URL, DOM, form values tùy chỉnh
- browser_click(text="..."): click theo text hiển thị — tự động fallback qua role/aria/scroll/vision nếu text không tìm thấy
- browser_fill: điền form
- browser_navigate: mở URL

Ưu tiên 2 — Chỉ dùng vision KHI DOM tools thất bại hoàn toàn:
- browser_vision_click: khi browser_click đã thất bại (đã thử hết 6 strategy)
- browser_vision_type: khi không tìm được selector input bằng bất kỳ cách nào
- browser_analyze_page: CHỈ khi cần hiểu layout CAPTCHA hoặc canvas UI thuần hình ảnh

KHÔNG BAO GIỜ:
- Gọi browser_analyze_page sau mỗi bước — dùng browser_get_dom_state hoặc browser_evaluate để verify
- Retry browser_analyze_page nhiều lần — nếu fail 1 lần, chuyển sang DOM tools
- Dùng vision để đọc text trang — dùng browser_evaluate("document.body.innerText")

Quy trình chuẩn cho mọi task web:
1. (Tuỳ chọn) browser_preflight_check(url) — kiểm tra nhanh trước khi load
2. browser_run_sequence([{navigate}, {fill_form}, {click}, {get_dom_state}]) — làm nhiều bước 1 lần gọi
   HOẶC từng bước riêng: browser_navigate → browser_get_dom_state → browser_fill_form / browser_click
3. browser_verify_action("success") hoặc browser_get_page_state() để xác nhận kết quả
KHÔNG cần browser_analyze_page cho 90% tasks thông thường.

Tip tối ưu:
- Research nhiều URL: dùng browser_parallel_fetch (song song, nhanh ~5x)
- Form login/register: dùng browser_fill_form(data={...}) thay vì fill từng field
- Task lặp lại: browser_macro_record → browser_macro_replay
- Tăng tốc trang text-only: browser_set_resource_blocking(block=["image","font","media"])
- Kiểm tra context session: browser_get_conv_context()
"""
# Khi bật: client chọn đúng MODEL (.env) thì route_model được dùng HAIKU_MODEL cho câu rất ngắn (tiết kiệm).
# Mặc định tắt — luôn gọi đúng model client gửi (tránh Haiku khi API key/proxy chưa đăng ký model đó).
_AGENT_SMART_MODEL_ROUTING = os.getenv("AGENT_SMART_MODEL_ROUTING", "").lower() in ("1", "true", "yes")


def _models_exclude_ids() -> set[str]:
    """Model id ẩn khỏi UI / không cho chọn (vd. API key trên proxy chưa đăng ký). MODELS_EXCLUDE=id1,id2"""
    raw = os.getenv("MODELS_EXCLUDE", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


DEFAULT_SYSTEM = """You are an AI Agent running on macOS. You can control the computer via tools.

CRITICAL — LANGUAGE RULE (highest priority, never override):
The user communicates in Vietnamese. You MUST reply in Vietnamese with FULL DIACRITICS at all times.
- CORRECT: "Bạn cần làm gì tiếp theo?" / "Đã lưu file thành công." / "Tôi hiểu yêu cầu của bạn."
- WRONG: "Ban can lam gi tiep theo?" / "Da luu file thanh cong." / "Toi hieu yeu cau cua ban."
- Every single word must have proper tone marks: à á ả ã ạ ă ắ ặ â ấ ầ ề ế ệ ỉ ị ó ọ ô ố ồ ơ ớ ờ ụ ư ứ ừ ỳ ỵ etc.
- This applies to ALL output: chat replies, tool call reasoning, summaries, lists, questions.
- UTF-8 is fully supported. Never strip accents for any reason.
- If you find yourself writing Vietnamese without diacritics, STOP and rewrite with full diacritics.

Formatting: Do not use emoji in replies. Use plain text labels (e.g. "CPU", "RAM") instead of symbols.

Speed: Prefer acting over long analysis. Call the right tool quickly; keep reasoning brief in text before tools. Use one tool per step when enough; avoid repeating plans.

Web / browser automation (critical for performance):
- Pages opened via browser_navigate / Playwright: prefer browser_evaluate (read DOM, forms, text), browser_fill, browser_click, browser_navigate — NOT screenshot_and_analyze after every tiny step.
- Use screenshot_and_analyze only when vision is truly needed (captcha, purely canvas/image UI, or desktop outside the browser). Do NOT loop: screenshot → act → screenshot → act repeatedly when DOM tools can verify state.
- After a click/fill, if you need to verify, use browser_evaluate (e.g. check URL, innerText, element existence) before considering another screenshot.
- Minimize total screenshot calls; each one is slow and expensive.

Do not describe automation (selectors, fake JS, or "step 1 open browser") as plain chat when the user expects real actions — call the tools so the server can execute them.

When given a task:
1. Check relevant memories first if needed
2. Use tools step by step
3. For web data: use run_shell with curl -s
4. Report results specifically in Vietnamese (with full diacritics) - include actual data
5. For structured data extraction, use the extract_data tool

Do NOT give vague reports. Always include real data.

""" + BROWSER_BEHAVIOR_PROMPT + BROWSER_VISION_STRATEGY_PROMPT

# Memory consolidation every 30 minutes
def _memory_consolidate_job():
    return memory_store.consolidate_old_memories(client)


scheduler.add_job(
    _memory_consolidate_job,
    "interval", minutes=30, id="memory_consolidation", replace_existing=True,
)

# Proactive event queue
_proactive_events = []
_proactive_lock = threading.Lock()

def _on_proactive_event(event_type: str, data: dict):
    with _proactive_lock:
        _proactive_events.append({"type": event_type, "data": data, "ts": datetime.now().isoformat()})
        if len(_proactive_events) > 100:
            _proactive_events.pop(0)

proactive_monitor.add_callback(_on_proactive_event)

# Tránh spam screenshot_and_analyze (mỗi lần = gọi vision API, rất chậm). 0 = tắt cooldown.
_SCREENSHOT_COOLDOWN_SEC = float(os.getenv("SCREENSHOT_COOLDOWN_SEC", "5") or "0")
_last_screenshot_mono: float = 0.0

TOOLS = [
    {"name": "run_shell", "description": "Run terminal/bash command on macOS",
     "input_schema": {"type": "object", "properties": {"cmd": {"type": "string"}}, "required": ["cmd"]}},
    {"name": "open_app", "description": "Open a macOS application. For web pages use browser_navigate instead of opening Chrome manually. Chrome is launched with a fixed profile to avoid the profile-picker screen.",
     "input_schema": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}},
    {"name": "run_applescript", "description": "Run AppleScript to control macOS apps",
     "input_schema": {"type": "object", "properties": {"script": {"type": "string"}}, "required": ["script"]}},
    {"name": "browser_navigate", "description": "Open URL in Chromium browser (human-like pacing, scroll/idle after load)",
     "input_schema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}},
    {"name": "browser_evaluate", "description": "Run JavaScript on current web page",
     "input_schema": {"type": "object", "properties": {"js": {"type": "string"}}, "required": ["js"]}},
    {"name": "browser_fill", "description": "Fill input on web page (human typing; use sensitive=true for passwords)",
     "input_schema": {"type": "object", "properties": {
         "selector": {"type": "string"},
         "value": {"type": "string"},
         "sensitive": {"type": "boolean", "description": "Faster typing, no typo simulation (passwords)"},
     }, "required": ["selector", "value"]}},
    {"name": "browser_click", "description": "Click element (Bezier mouse path). Provide selector OR text visible on page",
     "input_schema": {"type": "object", "properties": {
         "selector": {"type": "string", "description": "CSS selector (optional if text is set)"},
         "text": {"type": "string", "description": "Visible text to click (optional if selector is set)"},
     }, "required": []}},
    {"name": "browser_scroll", "description": "Scroll page naturally (human-like wheel steps)",
     "input_schema": {"type": "object", "properties": {
         "direction": {"type": "string", "enum": ["down", "up"], "description": "Scroll direction"},
         "amount": {"description": "small | medium | large | page | pixel count (int)"},
         "selector": {"type": "string", "description": "Optional: scroll this element into view first"},
     }, "required": []}},
    {"name": "browser_wait_for_human", "description": "Wait for load or selector with natural polling gaps",
     "input_schema": {"type": "object", "properties": {
         "condition": {"type": "string", "description": "CSS selector | navigation | network_idle"},
         "timeout_ms": {"type": "integer"},
     }, "required": ["condition"]}},
    {"name": "browser_new_tab", "description": "Mở tab mới trong browser",
     "input_schema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": []}},
    {"name": "browser_switch_tab", "description": "Chuyển sang tab theo index",
     "input_schema": {"type": "object", "properties": {"tab_id": {"type": "integer"}}, "required": ["tab_id"]}},
    {"name": "browser_list_tabs", "description": "Liệt kê tất cả tabs đang mở",
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "browser_close_tab", "description": "Đóng tab theo index",
     "input_schema": {"type": "object", "properties": {"tab_id": {"type": "integer"}}, "required": ["tab_id"]}},
    {"name": "browser_get_dom_state", "description": (
        "FAST — Lấy snapshot DOM trang hiện tại: URL, title, readyState, "
        "tất cả input/button/link visible, scroll position, alerts, modal. "
        "Dùng thay cho screenshot khi cần biết trang đang ở đâu sau navigate/click. "
        "Không tốn vision API — chạy thuần JavaScript."
    ),
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "browser_run_sequence", "description": (
        "FAST BATCH — Chạy danh sách actions tuần tự trong MỘT lần gọi, tiết kiệm nhiều LLM round-trips. "
        "Dùng cho login flows, form fill + submit, multi-step navigation. "
        "Actions: navigate, click, fill, fill_form, scroll, wait, wait_dom_stable, get_dom_state, evaluate, screenshot."
    ),
     "input_schema": {"type": "object", "properties": {
         "actions": {"type": "array", "description": "List các action dicts, ví dụ [{\"action\":\"navigate\",\"url\":\"...\"}]"},
     }, "required": ["actions"]}},
    {"name": "browser_fill_form", "description": (
        "Auto điền form bằng fuzzy-match — không cần CSS selector chính xác. "
        "Khớp key của data với name/id/placeholder/aria-label của input fields. "
        "Ví dụ: browser_fill_form(data={\"email\":\"...\",\"password\":\"...\"})"
    ),
     "input_schema": {"type": "object", "properties": {
         "data": {"type": "object", "description": "Dict field_name → value. Keys nên khớp với tên field (email, password, username, ...)"},
     }, "required": ["data"]}},
    {"name": "browser_set_resource_blocking", "description": (
        "Tăng tốc load trang bằng cách block loại tài nguyên không cần. "
        "block=[\"image\",\"font\",\"media\"] giúp load nhanh hơn 30-60% khi chỉ cần DOM/text. "
        "clear=true để tắt blocking."
    ),
     "input_schema": {"type": "object", "properties": {
         "block":   {"type": "array",   "description": "Resource types cần block: image, font, media, stylesheet, script, ..."},
         "unblock": {"type": "array",   "description": "Resource types cần bỏ block"},
         "clear":   {"type": "boolean", "description": "True = tắt toàn bộ blocking"},
     }, "required": []}},
    {"name": "browser_get_page_state", "description": (
        "FAST — Page State Machine: trả về state trang (LOADING/READY/FORM_VISIBLE/SUCCESS/ERROR/CAPTCHA). "
        "Thuần heuristics JS, không gọi vision. Dùng ngay sau click/submit để biết kết quả."
    ),
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "browser_parallel_fetch", "description": (
        "Fetch nhiều URL song song — tất cả cùng lúc, nhanh hơn ~5x so với tuần tự. "
        "Dùng cho research tasks: so sánh giá, scrape nhiều trang cùng chủ đề. "
        "Trả về JSON {url: result}."
    ),
     "input_schema": {"type": "object", "properties": {
         "urls":       {"type": "array",  "description": "List URLs cần fetch"},
         "extract_js": {"type": "string", "description": "JS expression để extract từ mỗi trang (mặc định: document.title)"},
     }, "required": ["urls"]}},
    {"name": "browser_verify_action", "description": (
        "DOM diff verify sau action — không cần screenshot. "
        "So sánh DOM state trước/sau để xác nhận action thành công. "
        "expected: url_changed | form_disappeared | alert_appeared | success | error | any_change"
    ),
     "input_schema": {"type": "object", "properties": {
         "expected":   {"type": "string",  "description": "Điều kiện cần verify"},
         "timeout_ms": {"type": "integer", "description": "Thời gian chờ DOM thay đổi (ms, mặc định 3000)"},
     }, "required": ["expected"]}},
    {"name": "browser_preflight_check", "description": (
        "Kiểm tra URL trước khi navigate: HTTP status, Cloudflare/bot detection, redirects. "
        "Dùng curl HEAD — không tốn Playwright load. Cảnh báo sớm nếu có block/403/429."
    ),
     "input_schema": {"type": "object", "properties": {
         "url": {"type": "string", "description": "URL cần kiểm tra"},
     }, "required": ["url"]}},
    {"name": "browser_macro_record", "description": "Bắt đầu ghi macro automation với tên cho trước. Mọi navigate/click/fill sau đó được record tự động.",
     "input_schema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
    {"name": "browser_macro_stop",   "description": "Dừng ghi macro và lưu vào library.",
     "input_schema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
    {"name": "browser_macro_replay", "description": "Replay macro đã lưu — chạy lại toàn bộ steps không cần LLM.",
     "input_schema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
    {"name": "browser_macro_list",   "description": "Liệt kê tất cả macros đã lưu.",
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "browser_get_conv_context", "description": (
        "Lấy browser context của conversation hiện tại: URL hiện tại, URLs đã visit, fields đã fill. "
        "Giúp Claude nhớ đang ở đâu mà không cần re-navigate."
    ),
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "browser_analyze_page", "description": (
        "SLOW & EXPENSIVE — Chụp screenshot và dùng AI vision phân tích layout. "
        "CHỈ dùng khi: (1) CAPTCHA/canvas UI không có DOM, (2) SPA với class hash không đoán được, "
        "(3) browser_click và browser_evaluate đã thất bại. "
        "KHÔNG dùng để verify sau navigate — dùng browser_get_dom_state thay thế. "
        "KHÔNG retry nếu fail — chuyển sang DOM tools."
    ),
     "input_schema": {"type": "object", "properties": {
         "focus": {"type": "string", "description": "Để trống = phân tích toàn viewport; hoặc mô tả phần cần chú ý"},
     }, "required": []}},
    {"name": "browser_vision_click", "description": (
        "Tìm và click element theo mô tả ngôn ngữ tự nhiên (vision). "
        "Tự động thử selector (nếu có) và text locator trước, sau đó mới gọi vision. "
        "Dùng khi browser_click(selector/text) thất bại hoặc DOM không ổn định."
    ),
     "input_schema": {"type": "object", "properties": {
         "target": {"type": "string", "description": "Mô tả element cần click, ví dụ 'nút Đăng nhập', 'link Quên mật khẩu'"},
         "verify": {"type": "boolean", "description": "Chụp ảnh sau click và hỏi vision xác nhận (mặc định true)"},
         "selector": {"type": "string", "description": "Tùy chọn: CSS selector — thử click nhanh trước khi tốn vision"},
     }, "required": []}},
    {"name": "browser_vision_type", "description": (
        "Tìm ô nhập theo mô tả (vision) rồi gõ text — không cần selector. "
        "Không dùng cho trường mật khẩu; dùng browser_fill(sensitive=true)."
    ),
     "input_schema": {"type": "object", "properties": {
         "target": {"type": "string", "description": "Mô tả field: 'ô email', 'ô tìm kiếm'"},
         "text": {"type": "string", "description": "Nội dung gõ vào"},
     }, "required": ["target", "text"]}},
    {"name": "screenshot_and_analyze", "description": "Desktop screenshot + vision (SLOW). For web pages already in the automated browser, prefer browser_evaluate / browser_click / browser_fill first. Use this for captchas, non-DOM visuals, or full-desktop context — not after every web action.",
     "input_schema": {"type": "object", "properties": {"question": {"type": "string"}}, "required": ["question"]}},
    {"name": "read_file", "description": "Read file content",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "write_file", "description": "Write content to file",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
    {"name": "notify", "description": "Send macOS notification. If the user uses Vietnamese, title and message must be standard Vietnamese with full diacritics (UTF-8).",
     "input_schema": {"type": "object", "properties": {
         "title": {"type": "string", "description": "Notification title (Vietnamese with diacritics when appropriate)"},
         "message": {"type": "string", "description": "Notification body (Vietnamese with diacritics when appropriate)"},
     }, "required": ["title", "message"]}},
    {"name": "schedule_task", "description": "Schedule a task to run after X seconds. Task description: use standard Vietnamese with diacritics when the user speaks Vietnamese.",
     "input_schema": {"type": "object", "properties": {"task": {"type": "string"}, "delay_seconds": {"type": "integer"}}, "required": ["task", "delay_seconds"]}},
    {"name": "remember", "description": "Save important information to long-term memory",
     "input_schema": {"type": "object", "properties": {"content": {"type": "string"}, "category": {"type": "string"}}, "required": ["content"]}},
    {"name": "recall", "description": "Search long-term memory for relevant information",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "extract_data", "description": "Trích xuất dữ liệu có cấu trúc từ văn bản theo JSON schema",
     "input_schema": {"type": "object", "properties": {
         "schema": {"type": "object", "description": "JSON schema cho output"},
         "source": {"type": "string", "description": "Văn bản nguồn cần trích xuất"},
     }, "required": ["schema", "source"]}},
]


def run_tool(name: str, inputs: dict) -> str:
    global _last_screenshot_mono
    try:
        if name == "run_shell":
            cmd = inputs["cmd"]
            if is_cacheable(cmd):
                cached = get_cached(cmd)
                if cached is not None:
                    return cached
            result = desktop.run_shell(cmd)
            if is_cacheable(cmd):
                set_cache(cmd, result)
            return result

        if name == "open_app":         return desktop.open_app(inputs["app_name"])
        if name == "run_applescript":  return desktop.run_applescript(inputs["script"])
        if name == "browser_navigate": return browser.navigate(inputs["url"])
        if name == "browser_evaluate": return browser.evaluate(inputs["js"])
        if name == "browser_fill":
            return browser.fill(
                inputs["selector"],
                inputs["value"],
                sensitive=bool(inputs.get("sensitive", False)),
            )
        if name == "browser_click":
            return browser.click_selector(
                inputs.get("selector") or None,
                inputs.get("text") or None,
            )
        if name == "browser_scroll":
            return browser.browser_scroll(
                inputs.get("direction", "down"),
                inputs.get("amount", "medium"),
                inputs.get("selector"),
            )
        if name == "browser_wait_for_human":
            return browser.browser_wait_for_human(
                inputs["condition"],
                int(inputs.get("timeout_ms", 10000)),
            )
        if name == "browser_new_tab":  return browser.new_tab(inputs.get("url", ""))
        if name == "browser_switch_tab": return browser.switch_tab(int(inputs["tab_id"]))
        if name == "browser_list_tabs":  return browser.list_tabs()
        if name == "browser_close_tab":  return browser.close_tab(int(inputs["tab_id"]))
        if name == "browser_get_dom_state": return browser.get_dom_state()
        if name == "browser_run_sequence":
            return browser.browser_run_sequence(inputs.get("actions", []))
        if name == "browser_fill_form":
            return browser.browser_fill_form(inputs.get("data", {}))
        if name == "browser_set_resource_blocking":
            return browser.browser_set_resource_blocking(
                block=inputs.get("block"),
                unblock=inputs.get("unblock"),
                clear=bool(inputs.get("clear", False)),
            )
        if name == "browser_get_page_state": return browser.get_page_state()
        if name == "browser_parallel_fetch":
            return browser.browser_parallel_fetch(
                urls=inputs.get("urls", []),
                extract_js=inputs.get("extract_js", "document.title"),
            )
        if name == "browser_verify_action":
            return browser.browser_verify_action(
                expected=str(inputs.get("expected", "any_change")),
                timeout_ms=int(inputs.get("timeout_ms", 3000)),
            )
        if name == "browser_preflight_check":
            return browser.browser_preflight_check(inputs["url"])
        if name == "browser_macro_record":  return browser.browser_macro_record(inputs["name"])
        if name == "browser_macro_stop":    return browser.browser_macro_stop(inputs["name"])
        if name == "browser_macro_replay":  return browser.browser_macro_replay(inputs["name"])
        if name == "browser_macro_list":    return browser.browser_macro_list()
        if name == "browser_get_conv_context": return browser.browser_get_conv_context()

        if name == "browser_analyze_page":
            return browser_analyze_page_tool(
                get_client(),
                DEFAULT_MODEL,
                (inputs.get("focus") or "").strip() or None,
            )
        if name == "browser_vision_click":
            return browser_vision_click_tool(
                get_client(),
                DEFAULT_MODEL,
                str(inputs.get("target") or ""),
                bool(inputs.get("verify", True)),
                (inputs.get("selector") or "").strip() or None,
            )
        if name == "browser_vision_type":
            return browser_vision_type_tool(
                get_client(),
                DEFAULT_MODEL,
                str(inputs.get("target") or ""),
                str(inputs.get("text") or ""),
            )

        if name == "read_file":
            p = os.path.expanduser(inputs["path"])
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                return f.read()[:8000]

        if name == "write_file":
            p = os.path.expanduser(inputs["path"])
            os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(inputs["content"])
            return f"Written: {p}"

        if name == "notify":
            _msg_esc = str(inputs.get("message", "")).replace("\\", "\\\\").replace('"', '\\"')
            _ttl_esc = str(inputs.get("title", "Oculo")).replace("\\", "\\\\").replace('"', '\\"')
            desktop.run_applescript(
                f'display notification "{_msg_esc}" with title "{_ttl_esc}"'
            )
            return f"Notification sent: {inputs.get('title', 'Oculo')}"

        if name == "schedule_task":
            job_id = str(uuid.uuid4())[:8]
            delay = int(inputs.get("delay_seconds", 0))
            task_desc = inputs.get("task", "")
            def run_scheduled():
                try:
                    msgs = [{"role": "user", "content": task_desc}]
                    max_rounds = 10
                    for _ in range(max_rounds):
                        r = get_client().messages.create(
                            model=DEFAULT_MODEL, max_tokens=2048,
                            system=DEFAULT_SYSTEM, tools=TOOLS, messages=msgs,
                        )
                        if r.stop_reason != "tool_use":
                            break
                        tool_results = []
                        for block in r.content:
                            if block.type == "tool_use":
                                result = run_tool(block.name, block.input)
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": result,
                                })
                        msgs.append({"role": "assistant", "content": serialize_content(r.content)})
                        msgs.append({"role": "user", "content": tool_results})
                    _td_esc = task_desc[:40].replace("\\", "\\\\").replace('"', '\\"')
                    desktop.run_applescript(
                        f'display notification "Task done: {_td_esc}" with title "Oculo"'
                    )
                except Exception as e:
                    print(f"Scheduled task error: {e}")
            scheduler.add_job(
                run_scheduled, "date",
                run_date=datetime.fromtimestamp(datetime.now().timestamp() + delay),
                id=job_id,
            )
            scheduled_jobs[job_id] = {"task": task_desc, "delay": delay, "created": datetime.now().isoformat()}
            return f"Scheduled '{task_desc}' in {delay}s (ID: {job_id})"

        if name == "screenshot_and_analyze":
            now = time.monotonic()
            if _SCREENSHOT_COOLDOWN_SEC > 0 and (now - _last_screenshot_mono) < _SCREENSHOT_COOLDOWN_SEC:
                wait = int(_SCREENSHOT_COOLDOWN_SEC - (now - _last_screenshot_mono)) + 1
                return (
                    "[Hệ thống — không gọi vision để tiết kiệm thời gian] "
                    "Hai lần chụp màn hình quá gần nhau. Với trang web trong browser automation, "
                    "hãy dùng browser_evaluate (đọc DOM, URL, text), browser_click, browser_fill. "
                    "Chỉ chụp lại khi thật sự cần pixel (captcha, v.v.). "
                    f"Thử lại sau ~{wait}s hoặc tăng khoảng cách giữa các lần chụp."
                )
            _last_screenshot_mono = now
            path = desktop.screenshot()
            with open(path, "rb") as f:
                img_b64 = base64.standard_b64encode(f.read()).decode()
            q = inputs.get("question", "Describe this screen")
            r = client.messages.create(
                model=DEFAULT_MODEL, max_tokens=1024,
                messages=[{"role": "user", "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                    {"type": "text", "text": q},
                ]}],
            )
            return _extract_text_from_content(r.content, "Error: no response from vision model")

        if name == "remember":
            doc_id = memory_store.save_memory(inputs["content"], {"category": inputs.get("category", "general")})
            return f"Saved to memory (ID: {doc_id})"

        if name == "recall":
            results = memory_store.search_memory(inputs["query"], n_results=5)
            if not results:
                return "No relevant memories found."
            return "\n".join([f"- [{r['metadata'].get('timestamp','')[:10]}] {r['content']}" for r in results])

        if name == "extract_data":
            schema = inputs.get("schema", {})
            source = inputs.get("source", "")
            if not schema or not source:
                return "Error: schema va source la bat buoc"
            extract_tool = {"name": "extracted", "description": "Structured output", "input_schema": schema}
            r = client.messages.create(
                model=DEFAULT_MODEL, max_tokens=1024,
                tools=[extract_tool],
                tool_choice={"type": "tool", "name": "extracted"},
                messages=[{"role": "user", "content": f"Extract data from:\n{source}"}],
            )
            for block in r.content:
                if block.type == "tool_use":
                    return json.dumps(block.input, ensure_ascii=False, indent=2)
            return "Error: khong trich xuat duoc du lieu"

        return f"Unknown tool: {name}"
    except Exception as e:
        return f"Error: {e}"


def run_tool_resilient(
    tool_name: str,
    tool_input: dict,
    yield_fn,
    task=None,
    step_index: int = 0,
) -> str:
    """
    Drop-in replacement cho run_tool() với full error recovery:
    classify → retry thông minh → fallback → partial progress save.

    yield_fn: callable(dict) để emit SSE event về frontend.
    """
    tool_fn = lambda **kwargs: run_tool(tool_name, kwargs)

    result_dict = run_with_retry(
        tool_fn=tool_fn,
        tool_name=tool_name,
        tool_input=tool_input,
        yield_fn=yield_fn,
    )

    if result_dict["success"]:
        if task:
            record_step(task, tool_name, tool_input,
                        result_dict["result"], "success",
                        result_dict["attempts"])
        return result_dict["result"]

    classified = result_dict.get("error")

    # Thử fallback
    if result_dict.get("should_fallback") and classified:
        yield_fn({
            "type": "fallback_attempt",
            "tool": tool_name,
            "message": f"Đang thử phương án dự phòng cho {tool_name}...",
            "category": classified.category.value,
        })
        fb = execute_fallback(tool_name, tool_input, run_tool)
        if fb["success"] and not fb.get("exhausted"):
            status = "skipped" if fb.get("skipped") else "success_via_fallback"
            if task:
                record_step(task, tool_name, tool_input,
                            fb["result"], status,
                            result_dict["attempts"],
                            classified.category.value)
            return fb["result"]

    # Abort — lưu progress để resume sau
    if task:
        record_step(task, tool_name, tool_input,
                    None, "failed",
                    result_dict["attempts"],
                    classified.category.value if classified else "unknown")
        task.status = "paused" if (classified and not classified.is_fatal()) else "failed"
        progress_store.save(task)

    # Trả về error string để agent biết và báo user
    if classified:
        return (
            f"Error: {classified.user_message} "
            f"[{classified.category.value}] "
            f"(task_id={task.task_id if task else 'n/a'}, "
            f"resumable={not classified.is_fatal()})"
        )
    return f"Error: {tool_name} thất bại sau {result_dict['attempts']} lần thử"


def serialize_content(blocks):
    out = []
    for b in blocks:
        if b.type == "text":
            out.append({"type": "text", "text": b.text})
        elif b.type == "tool_use":
            out.append({"type": "tool_use", "id": b.id, "name": b.name, "input": b.input})
        elif b.type == "thinking":
            out.append({"type": "thinking", "thinking": getattr(b, "thinking", "")})
        elif b.type == "redacted_thinking":
            out.append({"type": "redacted_thinking", "data": getattr(b, "data", "")})
    return out


def _anthropic_upstream_model_ids() -> list[str]:
    ml = client.models.list()
    return [m.id for m in ml]


def _merge_all_upstream_model_ids() -> tuple[list[str], set[str]]:
    """Anthropic + OpenAI-compat (Gemini) + Ollama local; trả về (danh sách gộp, id thuộc OpenAI-compat)."""
    ids: list[str] = []
    oai_set: set[str] = set()
    try:
        ids.extend(_anthropic_upstream_model_ids())
    except Exception as e:
        app.logger.warning("GET /models: Anthropic models.list: %s", e)
    if openai_compat_configured():
        try:
            oai = list_openai_compat_model_ids()
            oai_set = set(oai)
            ids.extend(oai)
        except Exception as e:
            app.logger.warning("GET /models: OpenAI-compat models.list: %s", e)
    try:
        ids.extend(_list_ollama_model_ids())
    except Exception as e:
        app.logger.warning("GET /models: Ollama models: %s", e)
    seen: set[str] = set()
    merged: list[str] = []
    for x in ids:
        if x and x not in seen:
            seen.add(x)
            merged.append(x)
    return merged, oai_set


def _stream_agent_openai_compat(
    user_content,
    history,
    abort_event,
    model,
    temperature,
    system_prompt,
    *,
    openai_client=None,
    ui_meta_override: dict | None = None,
    route_reason: str = "OpenAI-compat (Gemini)",
    allow_tools: bool = True,
):
    """Chat streaming qua OpenAI-compatible (vd. Gemini trên chiasegpu / Ollama local)."""
    from concurrent.futures import ThreadPoolExecutor
    from utils.openai_compat import get_openai_compat_client

    oai = openai_client or get_openai_compat_client()
    tools_oai = anthropic_tools_to_openai(TOOLS)

    query = _get_query_text(user_content)
    usage_tracker = TokenUsageTracker()
    key_manager.get_key()

    has_tool_history = any(
        isinstance(m.get("content"), list)
        and any(isinstance(c, dict) and c.get("type") == "tool_result" for c in m["content"])
        for m in history
    )
    routing = ModelRoutingDecision(model=model, complexity="user_specified", reason=route_reason)
    selected_model = model
    use_tools = bool(allow_tools) and should_use_tools(query, has_tool_history)
    active_tools_list = tools_oai if use_tools else []
    _mmu = ui_meta_override or model_ui_meta_openai_compat(selected_model)
    yield f"data: {json.dumps({'type': 'model_selected', 'model': selected_model, 'complexity': routing.complexity, 'reason': routing.reason, **_mmu})}\n\n"

    messages_for_compress = _trim_history_tool_results(list(history) + [{"role": "user", "content": user_content}])

    def _get_prefs():
        now = time.time()
        if now - _prefs_cache["ts"] < _PREFS_CACHE_TTL and _prefs_cache["obj"] is not None:
            return _prefs_cache["prompt"], _prefs_cache["obj"]
        prefs = load_preferences(memory_store)
        prompt = build_preference_prompt(prefs)
        _prefs_cache.update({"obj": prefs, "prompt": prompt, "ts": now})
        return prompt, prefs

    def _get_context():
        return _get_env_context_cached() if _should_inject_env_context(query) else ""

    def _get_memory():
        raw = memory_store.search_memory_with_scores(query, n_results=6)
        filtered = filter_memories(raw)
        return build_memory_context(filtered)

    def _compress():
        return compress_history(messages_for_compress, client)

    def _decompose():
        if not use_tools:
            return []
        if os.getenv("AGENT_SKIP_DECOMPOSE", "").lower() in ("1", "true", "yes"):
            return []
        return decompose_task(query, client)

    pref_prompt, prefs = "", None
    env_context = ""
    mem_context = ""
    compression_info = {}
    subtasks = []
    compressed_messages = messages_for_compress

    with ThreadPoolExecutor(max_workers=5) as ex:
        f_prefs = ex.submit(_get_prefs)
        f_ctx = ex.submit(_get_context)
        f_mem = ex.submit(_get_memory)
        f_compress = ex.submit(_compress)
        f_decomp = ex.submit(_decompose)
        try:
            pref_prompt, prefs = f_prefs.result(timeout=5)
        except Exception:
            pass
        try:
            env_context = f_ctx.result(timeout=8)
        except Exception:
            pass
        try:
            mem_context = f_mem.result(timeout=5)
        except Exception:
            pass
        try:
            compressed_messages, compression_info = f_compress.result(timeout=10)
        except Exception:
            pass
        try:
            subtasks = f_decomp.result(timeout=10)
        except Exception:
            pass

    if compression_info:
        yield f"data: {json.dumps({'type': 'history_compressed', 'compressed_count': compression_info.get('compressed_count', 0), 'summary_length': compression_info.get('summary_length', 0)})}\n\n"

    dynamic_parts = [p for p in [pref_prompt, env_context, mem_context] if p]
    if subtasks:
        plan_lines: list[str] = []
        for i, s in enumerate(subtasks[:6]):
            if isinstance(s, str) and s.strip():
                plan_lines.append(f"{i+1}. {s.strip()}")
        if plan_lines:
            dynamic_parts.append(
                "[Kế hoạch bắt buộc]\n"
                + "\n".join(plan_lines)
                + "\n\nYêu cầu: hãy thực hiện theo thứ tự. Sau khi hoàn tất mỗi subtask, xác nhận ngắn gọn và chỉ chuyển subtask tiếp theo khi đã đạt mục tiêu."
            )
    dynamic_system = "\n".join(dynamic_parts)
    cached_system = (
        build_cached_system(system_prompt, dynamic_system)
        if len(system_prompt.split()) >= 50
        else system_prompt + dynamic_system
    )
    system_str = flatten_cached_system(cached_system)

    messages = compressed_messages

    if subtasks:
        yield f"data: {json.dumps({'type': 'decomposition', 'subtasks': subtasks})}\n\n"

    while True:
        if abort_event.is_set():
            yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
            return

        if routing.complexity == "simple" and not active_tools_list:
            max_tokens = 1024
        elif active_tools_list:
            max_tokens = int(os.getenv("AGENT_TOOL_MAX_TOKENS", "8192"))
        else:
            max_tokens = int(os.getenv("AGENT_CHAT_MAX_TOKENS", "4096"))

        openai_messages = anthropic_messages_to_openai(messages, system_str)

        kwargs = dict(
            model=selected_model,
            messages=openai_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )
        if active_tools_list:
            kwargs["tools"] = active_tools_list

        text_acc: list[str] = []
        tool_parts: dict[int, dict] = {}
        finish_reason = None
        usage_obj = None

        def _run_stream(req_kwargs: dict):
            return oai.chat.completions.create(**req_kwargs)

        try:
            stream = _run_stream(kwargs)
            for chunk in stream:
                if abort_event.is_set():
                    yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
                    return
                u = getattr(chunk, "usage", None)
                if u:
                    usage_obj = u
                if not chunk.choices:
                    continue
                ch = chunk.choices[0]
                d = ch.delta
                if d:
                    if d.content:
                        text_acc.append(d.content)
                        yield f"data: {json.dumps({'type': 'text', 'content': d.content})}\n\n"
                    if d.tool_calls:
                        for tc in d.tool_calls:
                            idx = tc.index
                            if idx not in tool_parts:
                                tool_parts[idx] = {"id": None, "name": None, "arguments": ""}
                            if tc.id:
                                tool_parts[idx]["id"] = tc.id
                            if tc.function:
                                if tc.function.name:
                                    tool_parts[idx]["name"] = tc.function.name
                                if tc.function.arguments:
                                    tool_parts[idx]["arguments"] += tc.function.arguments
                if ch.finish_reason:
                    finish_reason = ch.finish_reason
        except Exception as stream_err:
            emsg = str(stream_err)
            # Một số backend OpenAI-compat (nhất là Ollama) không hỗ trợ tool/function-calling.
            # Nếu lỗi rõ ràng về tools, retry 1 lần không-tools để tránh fail "câu thứ 2".
            _tools_not_supported = (
                "does not support tools" in emsg.lower()
                or ("tool" in emsg.lower() and "not support" in emsg.lower())
                or ("tools" in emsg.lower() and "unsupported" in emsg.lower())
            )
            if active_tools_list and _tools_not_supported:
                try:
                    kwargs2 = dict(kwargs)
                    kwargs2.pop("tools", None)
                    active_tools_list = []
                    kwargs.pop("tools", None)
                    yield f"data: {json.dumps({'type': 'notice', 'content': 'Model hiện tại không hỗ trợ tools. Đang chuyển sang chế độ chat thuần (không tools).'} )}\n\n"
                    stream = _run_stream(kwargs2)
                    for chunk in stream:
                        if abort_event.is_set():
                            yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
                            return
                        u = getattr(chunk, "usage", None)
                        if u:
                            usage_obj = u
                        if not chunk.choices:
                            continue
                        ch = chunk.choices[0]
                        d = ch.delta
                        if d and d.content:
                            text_acc.append(d.content)
                            yield f"data: {json.dumps({'type': 'text', 'content': d.content})}\n\n"
                        if ch.finish_reason:
                            finish_reason = ch.finish_reason
                except Exception as stream_err2:
                    yield f"data: {json.dumps({'type': 'error', 'content': str(stream_err2)})}\n\n"
                    return
            else:
                yield f"data: {json.dumps({'type': 'error', 'content': emsg})}\n\n"
                return

        full_text = "".join(text_acc)
        response = build_openai_response_like_anthropic(finish_reason, full_text, tool_parts)
        response.usage = usage_from_openai(usage_obj)

        try:
            usage_tracker.update(response.usage)
        except Exception:
            pass

        if abort_event.is_set():
            yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
            return

        if response.stop_reason != "tool_use":
            yield f"data: {json.dumps({'type': 'token_usage', **usage_tracker.to_dict(selected_model)})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'stop_reason': response.stop_reason})}\n\n"

            def _bg_save():
                try:
                    all_text = " ".join([b.text for b in response.content if b.type == "text"])
                    if all_text and len(all_text) > 100:
                        memory_store.save_memory(
                            f"Session summary: User asked '{query[:100]}'. Agent responded: {all_text[:300]}",
                            {"category": "session", "type": "auto_summary"},
                        )
                    if prefs:
                        prefs.interaction_count += 1
                        detected = detect_preferences(query, len(all_text))
                        prefs.language = detected.get("language", prefs.language)
                        prefs.response_length = detected.get("response_length", prefs.response_length)
                        save_preferences(prefs, memory_store)
                except Exception:
                    pass

            threading.Thread(target=_bg_save, daemon=True).start()
            break

        tool_blocks = [b for b in response.content if b.type == "tool_use"]

        if can_run_parallel(tool_blocks):
            yield f"data: {json.dumps({'type': 'parallel_tools', 'count': len(tool_blocks)})}\n\n"
            parallel_results = run_tools_parallel(tool_blocks, run_tool)
            tool_results = []
            _blocks_by_id = {str(b.id): b for b in tool_blocks}
            for pr in parallel_results:
                summarized = maybe_summarize(pr["name"], pr["result"], None)
                masked, was_masked = mask_with_flag(summarized)
                tid = str(pr["tool_use_id"])
                blk = _blocks_by_id.get(tid)
                inp = blk.input if blk else {}
                yield f"data: {json.dumps({'type': 'tool_call', 'name': pr['name'], 'input': inp, 'id': tid})}\n\n"
                yield f"data: {json.dumps(_tool_result_payload(pr['name'], summarized, masked, was_masked, tid))}\n\n"
                tool_results.append({"type": "tool_result", "tool_use_id": pr["tool_use_id"], "content": summarized})
            for pie in browser.drain_page_intent_events():
                yield f"data: {json.dumps({'type': 'page_intent', **pie})}\n\n"
            for bfe in browser.drain_browser_frame_events():
                yield f"data: {json.dumps(bfe)}\n\n"
        else:
            tool_results = []
            _task = create_task(
                conversation_id="openai_compat",
                query=query,
                estimated_steps=len(tool_blocks),
            )
            for block in tool_blocks:
                if abort_event.is_set():
                    yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
                    return

                _cp_msgs = messages[:]
                threading.Thread(
                    target=lambda m, n: save_checkpoint(m, f"Before {n}"),
                    args=(_cp_msgs, block.name),
                    daemon=True,
                ).start()

                # Đọc nội dung file trước khi ghi (để diff)
                _before_content1 = None
                if block.name == "write_file" and block.input.get("path"):
                    try:
                        _fp1 = os.path.expanduser(block.input["path"])
                        if os.path.exists(_fp1):
                            with open(_fp1, "r", encoding="utf-8", errors="replace") as _bf1:
                                _before_content1 = _bf1.read()
                    except Exception:
                        pass

                _tool_call_payload1 = {'type': 'tool_call', 'name': block.name, 'input': block.input, 'id': str(block.id)}
                if _before_content1 is not None:
                    _tool_call_payload1['before_content'] = _before_content1[:8000]
                yield f"data: {json.dumps(_tool_call_payload1)}\n\n"

                if block.name == "run_shell":
                    cmd = block.input.get("cmd", "")
                    if is_cacheable(cmd):
                        cached = get_cached(cmd)
                        if cached is not None:
                            mf, wf = mask_with_flag(cached)
                            yield f"data: {json.dumps(_tool_result_payload(block.name, cached, mf, wf, block.id, cached=True))}\n\n"
                            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": cached})
                            record_step(_task, block.name, block.input, cached, "success", 1)
                            continue
                    full_output = []
                    shell_error = None
                    for line in desktop.run_shell_streaming(cmd):
                        if abort_event.is_set():
                            yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
                            return
                        if line == "__TIMEOUT__":
                            shell_error = "timeout"
                            yield f"data: {json.dumps({'type': 'tool_error', 'name': 'run_shell', 'error': 'timeout', 'tool_use_id': str(block.id)})}\n\n"
                            break
                        if line.startswith("__ERROR__"):
                            shell_error = line
                            yield f"data: {json.dumps({'type': 'tool_error', 'name': 'run_shell', 'error': line, 'tool_use_id': str(block.id)})}\n\n"
                            break
                        yield f"data: {json.dumps({'type': 'tool_stream', 'name': 'run_shell', 'line': line, 'tool_use_id': str(block.id)})}\n\n"
                        full_output.append(line)
                    result = "\n".join(full_output)
                    if shell_error and not result:
                        result = f"Error: {shell_error}"
                    if is_cacheable(cmd) and not shell_error:
                        set_cache(cmd, result)

                else:
                    _retry_events: list = []
                    result = run_tool_resilient(
                        tool_name=block.name,
                        tool_input=block.input,
                        yield_fn=_retry_events.append,
                        task=_task,
                        step_index=len(tool_results),
                    )
                    for ev in _retry_events:
                        yield f"data: {json.dumps(ev)}\n\n"
                    for pie in browser.drain_page_intent_events():
                        yield f"data: {json.dumps({'type': 'page_intent', **pie})}\n\n"
                    for bfe in browser.drain_browser_frame_events():
                        yield f"data: {json.dumps({**bfe, 'tool_use_id': str(block.id)})}\n\n"

                result = maybe_summarize(block.name, result, None)

                masked_result, was_masked = mask_with_flag(result)
                yield f"data: {json.dumps(_tool_result_payload(block.name, result, masked_result, was_masked, block.id))}\n\n"

                # Screenshot: gửi thumbnail b64 riêng để frontend hiện inline
                if block.name == "screenshot_and_analyze":
                    try:
                        _ss_path = desktop.screenshot()
                        with open(_ss_path, "rb") as _f:
                            _ss_b64 = base64.standard_b64encode(_f.read()).decode()
                        yield f"data: {json.dumps({'type':'screenshot_captured','tool_use_id':str(block.id),'b64':_ss_b64})}\n\n"
                    except Exception:
                        pass

                if block.name == "write_file" and not result.startswith("Error"):
                    if should_verify_write(block.input["path"], block.input["content"]):
                        v = verify_write_file(block.input["path"], block.input["content"], run_tool)
                        ev_type = "verification_passed" if v["success"] else "verification_failed"
                        yield f"data: {json.dumps({'type': ev_type, 'tool': 'write_file', 'detail': v})}\n\n"
                elif block.name == "browser_navigate" and not result.startswith("Error"):
                    if should_verify_navigate(block.input["url"]):
                        v = verify_browser_navigate(block.input["url"], run_tool)
                        ev_type = "verification_passed" if v["success"] else "verification_failed"
                        yield f"data: {json.dumps({'type': ev_type, 'tool': 'browser_navigate', 'detail': v})}\n\n"

                tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})

            if _task and not any(s.status == "failed" for s in _task.steps):
                progress_store.mark_completed(_task.task_id)

        messages.append({"role": "assistant", "content": serialize_content(response.content)})
        messages.append({"role": "user", "content": tool_results})


def stream_agent(user_content, history, abort_event, model, temperature, system_prompt, conv_id: str = ""):
    if _is_ollama_model_id(model):
        from openai import OpenAI

        ok, msg = _ensure_ollama_running()
        if not ok:
            yield f"data: {json.dumps({'type': 'error', 'content': f'Ollama chưa sẵn sàng: {msg}'})}\n\n"
            return

        selected_model = _normalize_ollama_model_id(model)
        if not selected_model:
            yield f"data: {json.dumps({'type': 'error', 'content': 'Model Ollama không hợp lệ.'})}\n\n"
            return

        oai = OpenAI(
            api_key=(os.getenv("OLLAMA_API_KEY") or "ollama"),
            base_url=f"{_OLLAMA_BASE_URL}/v1",
        )
        yield from _stream_agent_openai_compat(
            user_content,
            history,
            abort_event,
            selected_model,
            temperature,
            system_prompt,
            openai_client=oai,
            route_reason="Ollama local",
            allow_tools=(os.getenv("OLLAMA_ALLOW_TOOLS", "").lower() in ("1", "true", "yes")),
            ui_meta_override={
                "display_name": selected_model,
                "provider_label": "Ollama (local)",
                "route_hint": _OLLAMA_BASE_URL,
                "router_prefix": "ollama",
            },
        )
        return

    if openai_compat_configured() and is_openai_compat_model(model):
        yield from _stream_agent_openai_compat(
            user_content, history, abort_event, model, temperature, system_prompt
        )
        return

    from concurrent.futures import ThreadPoolExecutor
    query = _get_query_text(user_content)
    usage_tracker = TokenUsageTracker()

    # 1. Model routing + tool filtering (instant, no I/O)
    has_tool_history = any(
        isinstance(m.get("content"), list) and
        any(isinstance(c, dict) and c.get("type") == "tool_result" for c in m["content"])
        for m in history
    )
    routing = route_model(
        query,
        has_tool_history=has_tool_history,
        user_specified_model=(
            None
            if (_AGENT_SMART_MODEL_ROUTING and model == DEFAULT_MODEL)
            else model
        ),
    )
    selected_model = routing.model
    use_tools = should_use_tools(query, has_tool_history)
    active_tools = TOOLS if use_tools else []
    _mmu2 = model_ui_meta(selected_model)
    yield f"data: {json.dumps({'type': 'model_selected', 'model': selected_model, 'complexity': routing.complexity, 'reason': routing.reason, **_mmu2})}\n\n"

    # 2. Parallel pre-processing — chạy tất cả I/O blocking song song
    # Trước đây: tuần tự ~4-16s. Giờ: song song ~max(từng task)
    messages_for_compress = _trim_history_tool_results(list(history) + [{"role": "user", "content": user_content}])

    def _get_prefs():
        now = time.time()
        if now - _prefs_cache["ts"] < _PREFS_CACHE_TTL and _prefs_cache["obj"] is not None:
            return _prefs_cache["prompt"], _prefs_cache["obj"]
        prefs = load_preferences(memory_store)
        prompt = build_preference_prompt(prefs)
        _prefs_cache.update({"obj": prefs, "prompt": prompt, "ts": now})
        return prompt, prefs

    def _get_context():
        return _get_env_context_cached() if _should_inject_env_context(query) else ""

    def _get_memory():
        raw = memory_store.search_memory_with_scores(query, n_results=6)
        filtered = filter_memories(raw)
        return build_memory_context(filtered)

    def _compress():
        return compress_history(messages_for_compress, client)

    def _decompose():
        if not use_tools:
            return []
        if os.getenv("AGENT_SKIP_DECOMPOSE", "").lower() in ("1", "true", "yes"):
            return []
        return decompose_task(query, client)

    pref_prompt, prefs = "", None
    env_context = ""
    mem_context = ""
    compression_info = {}
    subtasks = []
    compressed_messages = messages_for_compress

    with ThreadPoolExecutor(max_workers=5) as ex:
        f_prefs   = ex.submit(_get_prefs)
        f_ctx     = ex.submit(_get_context)
        f_mem     = ex.submit(_get_memory)
        f_compress= ex.submit(_compress)
        f_decomp  = ex.submit(_decompose)

        try: pref_prompt, prefs = f_prefs.result(timeout=5)
        except Exception: pass
        try: env_context = f_ctx.result(timeout=8)
        except Exception: pass
        try: mem_context = f_mem.result(timeout=5)
        except Exception: pass
        try: compressed_messages, compression_info = f_compress.result(timeout=10)
        except Exception: pass
        try: subtasks = f_decomp.result(timeout=10)
        except Exception: pass

    if compression_info:
        yield f"data: {json.dumps({'type': 'history_compressed', 'compressed_count': compression_info.get('compressed_count', 0), 'summary_length': compression_info.get('summary_length', 0)})}\n\n"

    # 3. Build system prompt với prompt caching
    dynamic_parts = [p for p in [pref_prompt, env_context, mem_context] if p]
    if subtasks:
        plan_lines: list[str] = []
        for i, s in enumerate(subtasks[:6]):
            if isinstance(s, str) and s.strip():
                plan_lines.append(f"{i+1}. {s.strip()}")
        if plan_lines:
            dynamic_parts.append(
                "[Kế hoạch bắt buộc]\n"
                + "\n".join(plan_lines)
                + "\n\nYêu cầu: hãy thực hiện theo thứ tự. Sau khi hoàn tất mỗi subtask, hãy xác nhận ngắn gọn và chỉ chuyển bước tiếp theo khi đã đạt mục tiêu."
            )
    dynamic_system = "\n".join(dynamic_parts)
    cached_system = build_cached_system(system_prompt, dynamic_system) if len(system_prompt.split()) >= 50 else system_prompt + dynamic_system

    messages = compressed_messages

    # 4. Yield task checklist nếu có subtasks
    if subtasks:
        yield f"data: {json.dumps({'type': 'decomposition', 'subtasks': subtasks})}\n\n"

    # Main loop
    while True:
        if abort_event.is_set():
            yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
            return

        # Build API call kwargs
        # Dùng max_tokens nhỏ hơn cho query đơn giản → TTFT nhanh hơn
        if routing.complexity == "simple" and not active_tools:
            max_tokens = 1024
        elif active_tools:
            max_tokens = int(os.getenv("AGENT_TOOL_MAX_TOKENS", "8192"))
        else:
            max_tokens = int(os.getenv("AGENT_CHAT_MAX_TOKENS", "4096"))
        api_kwargs = dict(
            model=selected_model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
        )
        # System: list (cached) hoặc string
        if isinstance(cached_system, list):
            api_kwargs["system"] = cached_system
        else:
            api_kwargs["system"] = cached_system

        if active_tools:
            api_kwargs["tools"] = active_tools

        # Thêm betas header để kích hoạt prompt caching (nếu proxy hỗ trợ)
        _use_cache_beta = isinstance(api_kwargs.get("system"), list)
        if _use_cache_beta:
            api_kwargs["betas"] = ["prompt-caching-2024-07-31"]

        # Streaming — yield text tokens immediately as they arrive
        try:
            with get_client().messages.stream(**api_kwargs) as stream:
                for text_chunk in stream.text_stream:
                    if abort_event.is_set():
                        yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
                        return
                    yield f"data: {json.dumps({'type': 'text', 'content': text_chunk})}\n\n"
                response = stream.get_final_message()
        except Exception as stream_err:
            yield f"data: {json.dumps({'type': 'error', 'content': str(stream_err)})}\n\n"
            return

        # Track token usage
        try:
            usage_tracker.update(getattr(response, "usage", None))
        except Exception:
            pass

        if abort_event.is_set():
            yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
            return

        if response.stop_reason != "tool_use":
            # Yield done events FIRST — don't block on memory I/O
            yield f"data: {json.dumps({'type': 'token_usage', **usage_tracker.to_dict(selected_model)})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'stop_reason': response.stop_reason})}\n\n"

            # Memory + preference save in background — doesn't affect response time
            def _bg_save():
                try:
                    all_text = " ".join([b.text for b in response.content if b.type == "text"])
                    if all_text and len(all_text) > 100:
                        memory_store.save_memory(
                            f"Session summary: User asked '{query[:100]}'. Agent responded: {all_text[:300]}",
                            {"category": "session", "type": "auto_summary"},
                        )
                    if prefs:
                        prefs.interaction_count += 1
                        detected = detect_preferences(query, len(all_text))
                        prefs.language = detected.get("language", prefs.language)
                        prefs.response_length = detected.get("response_length", prefs.response_length)
                        save_preferences(prefs, memory_store)
                except Exception:
                    pass
            threading.Thread(target=_bg_save, daemon=True).start()
            break

        tool_blocks = [b for b in response.content if b.type == "tool_use"]

        # Parallel execution
        if can_run_parallel(tool_blocks):
            yield f"data: {json.dumps({'type': 'parallel_tools', 'count': len(tool_blocks)})}\n\n"
            parallel_results = run_tools_parallel(tool_blocks, run_tool)
            tool_results = []
            _blocks_by_id2 = {str(b.id): b for b in tool_blocks}
            for pr in parallel_results:
                summarized = maybe_summarize(pr["name"], pr["result"], client)
                masked, was_masked = mask_with_flag(summarized)
                tid = str(pr["tool_use_id"])
                blk = _blocks_by_id2.get(tid)
                inp = blk.input if blk else {}
                yield f"data: {json.dumps({'type': 'tool_call', 'name': pr['name'], 'input': inp, 'id': tid})}\n\n"
                yield f"data: {json.dumps(_tool_result_payload(pr['name'], summarized, masked, was_masked, tid))}\n\n"
                tool_results.append({"type": "tool_result", "tool_use_id": pr["tool_use_id"], "content": summarized})
            for pie in browser.drain_page_intent_events():
                yield f"data: {json.dumps({'type': 'page_intent', **pie})}\n\n"
            for bfe in browser.drain_browser_frame_events():
                yield f"data: {json.dumps(bfe)}\n\n"
        else:
            tool_results = []
            _task = create_task(
                conversation_id=conv_id or "unknown",
                query=query,
                estimated_steps=len(tool_blocks),
            )
            for block in tool_blocks:
                if abort_event.is_set():
                    yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
                    return

                # Checkpoint save chạy nền
                _cp_msgs = messages[:]
                threading.Thread(
                    target=lambda m, n: save_checkpoint(m, f"Before {n}"),
                    args=(_cp_msgs, block.name), daemon=True
                ).start()

                # Đọc nội dung file trước khi ghi (để diff)
                _before_content2 = None
                if block.name == "write_file" and block.input.get("path"):
                    try:
                        _fp2 = os.path.expanduser(block.input["path"])
                        if os.path.exists(_fp2):
                            with open(_fp2, "r", encoding="utf-8", errors="replace") as _bf2:
                                _before_content2 = _bf2.read()
                    except Exception:
                        pass

                _tool_call_payload2 = {'type': 'tool_call', 'name': block.name, 'input': block.input, 'id': str(block.id)}
                if _before_content2 is not None:
                    _tool_call_payload2['before_content'] = _before_content2[:8000]
                yield f"data: {json.dumps(_tool_call_payload2)}\n\n"

                if block.name == "run_shell":
                    cmd = block.input.get("cmd", "")
                    if is_cacheable(cmd):
                        cached = get_cached(cmd)
                        if cached is not None:
                            mf, wf = mask_with_flag(cached)
                            yield f"data: {json.dumps(_tool_result_payload(block.name, cached, mf, wf, block.id, cached=True))}\n\n"
                            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": cached})
                            record_step(_task, block.name, block.input, cached, "success", 1)
                            continue
                    full_output = []
                    shell_error = None
                    for line in desktop.run_shell_streaming(cmd):
                        if abort_event.is_set():
                            yield f"data: {json.dumps({'type': 'interrupted'})}\n\n"
                            return
                        if line == "__TIMEOUT__":
                            shell_error = "timeout"
                            yield f"data: {json.dumps({'type': 'tool_error', 'name': 'run_shell', 'error': 'timeout', 'tool_use_id': str(block.id)})}\n\n"
                            break
                        if line.startswith("__ERROR__"):
                            shell_error = line
                            yield f"data: {json.dumps({'type': 'tool_error', 'name': 'run_shell', 'error': line, 'tool_use_id': str(block.id)})}\n\n"
                            break
                        yield f"data: {json.dumps({'type': 'tool_stream', 'name': 'run_shell', 'line': line, 'tool_use_id': str(block.id)})}\n\n"
                        full_output.append(line)
                    result = "\n".join(full_output)
                    if shell_error and not result:
                        result = f"Error: {shell_error}"
                    if is_cacheable(cmd) and not shell_error:
                        set_cache(cmd, result)

                else:
                    # Tất cả tools khác: dùng run_tool_resilient
                    _retry_events: list = []
                    result = run_tool_resilient(
                        tool_name=block.name,
                        tool_input=block.input,
                        yield_fn=_retry_events.append,
                        task=_task,
                        step_index=len(tool_results),
                    )
                    for ev in _retry_events:
                        yield f"data: {json.dumps(ev)}\n\n"
                    for pie in browser.drain_page_intent_events():
                        yield f"data: {json.dumps({'type': 'page_intent', **pie})}\n\n"
                    for bfe in browser.drain_browser_frame_events():
                        yield f"data: {json.dumps({**bfe, 'tool_use_id': str(block.id)})}\n\n"

                # Tool summarization
                result = maybe_summarize(block.name, result, client)

                # Mask sensitive data before yielding to client
                masked_result, was_masked = mask_with_flag(result)
                yield f"data: {json.dumps(_tool_result_payload(block.name, result, masked_result, was_masked, block.id))}\n\n"

                # Screenshot: gửi thumbnail b64 riêng để frontend hiện inline
                if block.name == "screenshot_and_analyze":
                    try:
                        _ss_path = desktop.screenshot()
                        with open(_ss_path, "rb") as _f:
                            _ss_b64 = base64.standard_b64encode(_f.read()).decode()
                        yield f"data: {json.dumps({'type':'screenshot_captured','tool_use_id':str(block.id),'b64':_ss_b64})}\n\n"
                    except Exception:
                        pass

                # Lazy self-correction
                if block.name == "write_file" and not result.startswith("Error"):
                    if should_verify_write(block.input["path"], block.input["content"]):
                        v = verify_write_file(block.input["path"], block.input["content"], run_tool)
                        ev_type = "verification_passed" if v["success"] else "verification_failed"
                        yield f"data: {json.dumps({'type': ev_type, 'tool': 'write_file', 'detail': v})}\n\n"
                elif block.name == "browser_navigate" and not result.startswith("Error"):
                    if should_verify_navigate(block.input["url"]):
                        v = verify_browser_navigate(block.input["url"], run_tool)
                        ev_type = "verification_passed" if v["success"] else "verification_failed"
                        yield f"data: {json.dumps({'type': ev_type, 'tool': 'browser_navigate', 'detail': v})}\n\n"

                tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})

            # Mark task completed nếu không có bước nào failed
            if _task and not any(s.status == "failed" for s in _task.steps):
                progress_store.mark_completed(_task.task_id)

        messages.append({"role": "assistant", "content": serialize_content(response.content)})
        messages.append({"role": "user", "content": tool_results})


def _to_bool(value, default=False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("1", "true", "yes", "on"):
            return True
        if v in ("0", "false", "no", "off"):
            return False
    return default


def _ollama_bin_exists() -> bool:
    return bool(shutil.which("ollama"))


def _ollama_health_ok(timeout_s: float = 0.5) -> bool:
    try:
        req = urlrequest.Request(f"{_OLLAMA_BASE_URL}/api/tags", method="GET")
        with urlrequest.urlopen(req, timeout=timeout_s) as resp:
            return 200 <= int(getattr(resp, "status", 0)) < 300
    except Exception:
        return False


def _normalize_ollama_model_id(model_id: str | None) -> str:
    mid = (model_id or "").strip()
    if not mid:
        return ""
    low = mid.lower()
    if low.startswith("ollama/"):
        return mid.split("/", 1)[1].strip()
    if low.startswith("ollama:"):
        return mid.split(":", 1)[1].strip()
    return mid


def _is_ollama_model_id(model_id: str | None) -> bool:
    mid = (model_id or "").strip()
    if not mid:
        return False
    low = mid.lower()
    if low == "ollama" or low.startswith("ollama/") or low.startswith("ollama:"):
        return True
    if "/" in low and low.split("/", 1)[0] == "ollama":
        return True
    meta = model_ui_meta(mid)
    if str(meta.get("router_prefix") or "").lower() == "ollama":
        return True
    return "ollama" in str(meta.get("provider_label") or "").lower()


def _list_ollama_model_ids(refresh: bool = False) -> list[str]:
    now = time.time()
    if (
        not refresh
        and (now - float(_ollama_models_cache.get("ts", 0.0))) < _OLLAMA_MODELS_TTL
        and isinstance(_ollama_models_cache.get("items"), list)
    ):
        return list(_ollama_models_cache["items"])

    # Nếu Ollama chưa chạy nhưng có binary, thử tự bật để lấy danh sách model local.
    if not _ollama_health_ok(timeout_s=0.8):
        if _ollama_bin_exists():
            try:
                _ensure_ollama_running(timeout_s=2.0)
            except Exception:
                pass
        if not _ollama_health_ok(timeout_s=0.8):
            _ollama_models_cache.update({"ts": now, "items": []})
            return []

    try:
        req = urlrequest.Request(f"{_OLLAMA_BASE_URL}/api/tags", method="GET")
        with urlrequest.urlopen(req, timeout=2.0) as resp:
            raw = json.loads(resp.read().decode("utf-8", errors="replace") or "{}")
        models = raw.get("models", []) if isinstance(raw, dict) else []
        ids = []
        for m in models:
            name = str((m or {}).get("name") or "").strip()
            if name:
                ids.append(f"ollama/{name}")
        # unique giữ thứ tự
        out = list(dict.fromkeys(ids))
        _ollama_models_cache.update({"ts": now, "items": out})
        return out
    except Exception:
        _ollama_models_cache.update({"ts": now, "items": []})
        return []


def _ensure_ollama_running(timeout_s: float = 8.0) -> tuple[bool, str]:
    global _ollama_service_proc
    if not _ollama_bin_exists():
        return False, "Không tìm thấy binary 'ollama' trong PATH."
    if _ollama_health_ok(timeout_s=0.7):
        return True, "already_running"

    # Serialize spawn + avoid double-spawn under concurrent requests.
    with _ollama_spawn_lock:
        if _ollama_health_ok(timeout_s=0.7):
            return True, "already_running"
        if _ollama_service_proc is not None and _ollama_service_proc.poll() is None:
            # Someone already spawned it; fall through to wait loop.
            pass
        else:
            try:
                # On Apple Silicon (ex: M5/M6), ggml Metal sometimes triggers on-the-fly compilation
                # and the runner may get killed during model load. Disable Metal tensors by default.
                _env = os.environ.copy()
                _env.setdefault("GGML_METAL_TENSOR_DISABLE", "1")
                _ollama_service_proc = subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                    env=_env,
                )
            except Exception as e:
                return False, f"Không thể chạy ollama serve: {e}"

    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if _ollama_health_ok(timeout_s=0.7):
            return True, "started"
        if _ollama_service_proc and _ollama_service_proc.poll() is not None:
            return False, "ollama serve thoát sớm."
        time.sleep(0.25)
    return False, "Khởi động Ollama quá thời gian chờ."


def _fallback_non_ollama_model() -> str:
    candidates: list[str] = []
    for mid in (DEFAULT_MODEL, os.getenv("MODEL"), os.getenv("HAIKU_MODEL"), os.getenv("GEMINI_MODEL")):
        if mid:
            candidates.append(mid)
    try:
        merged, _ = _merge_all_upstream_model_ids()
        candidates.extend(merged)
    except Exception:
        pass

    excluded = _models_exclude_ids()
    seen: set[str] = set()
    for mid in candidates:
        m = str(mid or "").strip()
        if not m or m in seen or m in excluded:
            continue
        seen.add(m)
        if not _is_ollama_model_id(m):
            return m
    return DEFAULT_MODEL


# ── Routes ──

@app.route("/")
def index():
    return send_from_directory(_STATIC_DIR, "index.html")

@app.route("/static/sw.js")
def service_worker():
    resp = send_from_directory(_STATIC_DIR, "sw.js")
    resp.headers["Service-Worker-Allowed"] = "/"
    resp.headers["Cache-Control"] = "no-cache"
    return resp


@app.route("/chat", methods=["POST"])
def chat():
    # Rate limiting
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if not _check_rate_limit(client_ip):
        return jsonify({"error": "Too many requests. Please slow down."}), 429

    data      = request.get_json(silent=True) or {}
    message   = data.get("message", "")
    files     = data.get("files", [])
    history   = data.get("history", [])
    model     = data.get("model", DEFAULT_MODEL)
    if model in _models_exclude_ids():
        model = DEFAULT_MODEL
    use_ollama = _to_bool(data.get("use_ollama"), True)
    if not use_ollama and _is_ollama_model_id(model):
        model = _fallback_non_ollama_model()
    temp      = float(data.get("temperature", DEFAULT_TEMP))
    system    = data.get("system_prompt") or DEFAULT_SYSTEM
    stream_id = data.get("stream_id", str(uuid.uuid4()))
    conv_id   = data.get("conv_id", stream_id)
    try:
        browser.set_browser_conv_id(conv_id)
    except Exception:
        pass

    abort_event = threading.Event()
    active_streams[stream_id] = abort_event

    if files:
        user_content = [{"type": "text", "text": message}]
        for f in files:
            ftype = f.get("type", "")
            fdata = f.get("data", "")
            fname = f.get("name", "file")
            if not fdata:
                continue
            if ftype.startswith("image/"):
                user_content.append({"type": "image", "source": {"type": "base64", "media_type": ftype, "data": _resize_image_b64(fdata, ftype)}})
            else:
                try:
                    text = base64.b64decode(fdata).decode("utf-8", errors="replace")
                    user_content.append({"type": "text", "text": f"\n\n--- File: {fname} ---\n{text[:4000]}"})
                except Exception:
                    pass
    else:
        user_content = message

    def generate():
        try:
            for event in stream_agent(user_content, history, abort_event, model, temp, system, conv_id=conv_id):
                yield event
        except Exception as e:
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        finally:
            active_streams.pop(stream_id, None)

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/pipeline", methods=["POST"])
def pipeline():
    data = request.get_json(silent=True) or {}
    task = data.get("task", "")
    if not task:
        return jsonify({"error": "task required"}), 400

    def generate():
        try:
            for event in run_pipeline(task, client):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            traceback.print_exc()
            yield f"data: {json.dumps({'stage': 'error', 'content': str(e)})}\n\n"

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/computer-use", methods=["POST"])
def computer_use():
    from computer_use.controller import run_computer_use
    data = request.get_json(silent=True) or {}
    task = data.get("task", "")
    if not task:
        return jsonify({"error": "task required"}), 400

    cu_client = get_optional_anthropic_direct()
    if not cu_client:
        return jsonify({
            "error": (
                "Computer Use cần Anthropic Messages API (beta). "
                "Thêm ANTHROPIC_API_KEY vào .env (Messages API trực tiếp)."
            ),
        }), 501

    def generate():
        try:
            for event in run_computer_use(task, cu_client):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/memory", methods=["GET"])
def get_memories():
    return jsonify(memory_store.list_memories(limit=50))

@app.route("/memory", methods=["POST"])
def add_memory():
    data = request.get_json(silent=True) or {}
    doc_id = memory_store.save_memory(data.get("content", ""), data.get("metadata", {}))
    return jsonify({"ok": True, "id": doc_id})

@app.route("/memory/search", methods=["POST"])
def search_memory():
    query = (request.get_json(silent=True) or {}).get("query", "")
    results = memory_store.search_memory(query)
    return jsonify(results)

@app.route("/memory/<doc_id>", methods=["DELETE"])
def delete_memory(doc_id):
    memory_store.delete_memory(doc_id)
    return jsonify({"ok": True})

@app.route("/memory/clear", methods=["POST"])
def clear_memory():
    memory_store.clear_all_memories()
    return jsonify({"ok": True})

@app.route("/memory/consolidate", methods=["POST"])
def consolidate_memory():
    result = memory_store.consolidate_old_memories(client)
    return jsonify(result)


@app.route("/monitors", methods=["GET"])
def get_monitors():
    return jsonify(proactive_monitor.list_monitors())

@app.route("/monitors/file", methods=["POST"])
def start_file_monitor():
    data = request.get_json(silent=True) or {}
    result = proactive_monitor.start_file_monitor(
        data.get("id", str(uuid.uuid4())[:8]),
        data.get("path", "~/Desktop"),
        data.get("patterns", []),
    )
    return jsonify(result)

@app.route("/monitors/calendar", methods=["POST"])
def start_calendar_monitor():
    data = request.get_json(silent=True) or {}
    result = proactive_monitor.start_calendar_monitor(
        data.get("id", str(uuid.uuid4())[:8]),
        data.get("interval_minutes", 5),
    )
    return jsonify(result)

@app.route("/monitors/system", methods=["POST"])
def start_system_monitor():
    data = request.get_json(silent=True) or {}
    result = proactive_monitor.start_system_monitor(
        data.get("id", str(uuid.uuid4())[:8]),
        data.get("cpu_threshold", 90.0),
        data.get("mem_threshold", 90.0),
        data.get("interval", 30),
    )
    return jsonify(result)

@app.route("/monitors/<watch_id>", methods=["DELETE"])
def stop_monitor(watch_id):
    return jsonify(proactive_monitor.stop_monitor(watch_id))

@app.route("/monitors/events", methods=["GET"])
def get_proactive_events():
    with _proactive_lock:
        return jsonify(list(_proactive_events))


@app.route("/abort/<stream_id>", methods=["POST"])
def abort(stream_id):
    ev = active_streams.get(stream_id)
    if ev:
        ev.set()
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Stream not found"}), 404


@app.route("/notify-client", methods=["POST"])
def notify_client():
    """Thông báo macOS trực tiếp (ambient widget done) — không qua LLM/tool notify."""
    data = request.get_json(silent=True) or {}
    title = str(data.get("title") or "Oculo")[:200]
    body = str(data.get("body") or "")[:500]
    t_esc = title.replace("\\", "\\\\").replace('"', '\\"')
    b_esc = body.replace("\\", "\\\\").replace('"', '\\"')
    try:
        desktop.run_applescript(f'display notification "{b_esc}" with title "{t_esc}"')
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    return jsonify({"ok": True})

@app.route("/schedules", methods=["GET"])
def get_schedules():
    return jsonify(scheduled_jobs)

@app.route("/schedules/<job_id>", methods=["DELETE"])
def delete_schedule(job_id):
    try:
        scheduler.remove_job(job_id)
        scheduled_jobs.pop(job_id, None)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

def _merge_env_model_ids(ids: list[str]) -> list[str]:
    """Giữ thứ tự upstream, thêm MODEL / HAIKU_MODEL từ .env nếu chưa có (fallback khi upstream thiếu hoặc lỗi)."""
    seen: set[str] = set()
    out: list[str] = []
    for x in ids:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    for mid in (os.getenv("MODEL"), os.getenv("HAIKU_MODEL"), os.getenv("GEMINI_MODEL")):
        if mid and mid not in seen:
            seen.add(mid)
            out.append(mid)
    return out


@app.route("/models", methods=["GET"])
def get_models():
    merged: list[str] = []
    oai_set: set[str] = set()
    try:
        merged, oai_set = _merge_all_upstream_model_ids()
    except Exception as e:
        app.logger.warning("GET /models: %s", e)
    ids = _merge_env_model_ids(merged)
    exc = _models_exclude_ids()
    if exc:
        ids = [x for x in ids if x not in exc]
    if not ids:
        ids = [DEFAULT_MODEL]
    oai_labels = set(oai_set)
    if openai_compat_configured():
        for raw in (os.getenv("GEMINI_MODEL", ""), os.getenv("GEMINI_EXTRA_MODELS", "")):
            for p in raw.split(","):
                t = p.strip()
                if t:
                    oai_labels.add(t)
    resp = jsonify(enrich_models_list(ids, openai_compat_ids=oai_labels))
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    return resp


@app.route("/client-config", methods=["GET"])
def client_config():
    """default_model + exclude_model_ids — đồng bộ UI với MODELS_EXCLUDE / MODEL."""
    exc = sorted(_models_exclude_ids())
    resp = jsonify(
        {
            "default_model": DEFAULT_MODEL,
            "exclude_model_ids": exc,
            "app_name": APP_NAME,
            "app_version": APP_VERSION,
            # Optional: where client can check for updates (JSON feed or GitHub API proxy).
            "update_feed_url": (os.getenv("OCULO_UPDATE_FEED_URL") or "").strip(),
            "downloads_url": (os.getenv("OCULO_DOWNLOADS_URL") or "").strip(),
        }
    )
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return resp


@app.route("/version", methods=["GET"])
def version():
    return jsonify({"name": APP_NAME, "version": APP_VERSION})


@app.route("/update/open", methods=["POST"])
def update_open():
    """
    Open a URL (e.g. dmg download page) on the user's Mac.
    This avoids complicated in-place self-update.
    """
    data = request.get_json(silent=True) or {}
    url = str(data.get("url") or "").strip()
    if not (url.startswith("https://") or url.startswith("http://")):
        return jsonify({"ok": False, "error": "invalid url"}), 400
    try:
        import webbrowser
        webbrowser.open(url)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/ollama/status", methods=["GET"])
def ollama_status():
    running = _ollama_health_ok(timeout_s=0.8)
    installed = _ollama_bin_exists()
    models = _list_ollama_model_ids() if running else []
    return jsonify(
        {
            "installed": installed,
            "running": running,
            "base_url": _OLLAMA_BASE_URL,
            "models": models,
        }
    )


@app.route("/ollama/enable", methods=["POST"])
def ollama_enable():
    ok, msg = _ensure_ollama_running()
    models = _list_ollama_model_ids(refresh=True) if ok else []
    status = {
        "ok": ok,
        "message": msg,
        "installed": _ollama_bin_exists(),
        "running": _ollama_health_ok(timeout_s=0.8),
        "base_url": _OLLAMA_BASE_URL,
        "models": models,
    }
    return jsonify(status), 200 if ok else 503


# ── Checkpoints ──
@app.route("/checkpoints", methods=["GET"])
def get_checkpoints():
    return jsonify(list_checkpoints())

@app.route("/checkpoints/<cp_id>/restore", methods=["POST"])
def restore_cp(cp_id):
    msgs = restore_checkpoint(cp_id)
    if msgs is None:
        return jsonify({"error": "Checkpoint not found"}), 404
    return jsonify({"messages": msgs})


# ── Generate title ──
@app.route("/generate-title", methods=["POST"])
def generate_title():
    messages = (request.get_json(silent=True) or {}).get("messages", [])
    if not messages:
        return jsonify({"title": "Cuộc hội thoại mới"})
    sample = " ".join([
        m.get("content", "")[:100]
        for m in messages[:3]
        if isinstance(m.get("content"), str)
    ])
    try:
        mdl = os.getenv("HAIKU_MODEL") or os.getenv("MODEL", DEFAULT_MODEL)
        prompt = f"Đặt tiêu đề ngắn (tối đa 5 từ) cho cuộc hội thoại này, tiếng Việt chuẩn có đầy đủ dấu: {sample}"
        r = client.messages.create(
            model=mdl,
            max_tokens=30,
            messages=[{"role": "user", "content": prompt}],
        )
        title = _extract_text_from_content(r.content, "Cuộc hội thoại")
        title = title.strip().strip('"\'')
        return jsonify({"title": title[:50]})
    except Exception:
        return jsonify({"title": "Cuộc hội thoại"})


@app.route("/list-files", methods=["GET"])
def list_files():
    """Liệt kê files từ Desktop và Downloads để @ mention."""
    import glob as _glob
    query = request.args.get("q", "").lower().strip()
    results = []
    search_dirs = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Documents"),
    ]
    seen = set()
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        try:
            for fname in sorted(os.listdir(d))[:40]:
                fpath = os.path.join(d, fname)
                if fname.startswith('.') or not os.path.isfile(fpath):
                    continue
                if query and query not in fname.lower():
                    continue
                if fpath in seen:
                    continue
                seen.add(fpath)
                results.append({"name": fname, "path": fpath})
                if len(results) >= 20:
                    break
        except Exception:
            pass
        if len(results) >= 20:
            break
    return jsonify(results)


_READ_FILE_ALLOWED_DIRS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Documents"),
]

@app.route("/read-file-b64", methods=["POST"])
def read_file_b64():
    """Đọc file và trả về base64 để attach vào chat."""
    path = (request.get_json(silent=True) or {}).get("path", "")
    if not path:
        return jsonify({"error": "path required"}), 400
    path = os.path.realpath(os.path.expanduser(path))
    if not any(path.startswith(d + os.sep) or path == d for d in _READ_FILE_ALLOWED_DIRS):
        return jsonify({"error": "access denied: path outside allowed directories"}), 403
    if not os.path.isfile(path):
        return jsonify({"error": "file not found"}), 404
    try:
        import mimetypes as _mt
        mime = _mt.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            b64 = base64.standard_b64encode(f.read(2 * 1024 * 1024)).decode()  # max 2MB
        return jsonify({"b64": b64, "mime": mime})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/suggest-followups", methods=["POST"])
def suggest_followups():
    """Gợi ý tiếp theo thông minh: mix câu hỏi + hành động dựa trên context tools."""
    data = request.get_json(silent=True) or {}
    question   = data.get("question",   "")[:400]
    answer     = data.get("answer",     "")[:600]
    tool_names = data.get("tool_names", [])
    if not question:
        return jsonify({"suggestions": []})
    try:
        mdl = os.getenv("HAIKU_MODEL") or os.getenv("MODEL", DEFAULT_MODEL)

        # Xây context tools để model biết đã làm gì
        tools_ctx = ""
        if tool_names:
            tool_label_map = {
                "run_shell": "chạy lệnh terminal",
                "write_file": "ghi file",
                "read_file": "đọc file",
                "browser_navigate": "duyệt web",
                "browser_click": "click trên web",
                "browser_fill": "điền form web",
                "screenshot_and_analyze": "chụp & phân tích màn hình",
                "remember": "lưu bộ nhớ",
                "recall": "truy vấn bộ nhớ",
                "open_app": "mở ứng dụng",
                "schedule_task": "lên lịch tác vụ",
                "notify": "gửi thông báo",
                "extract_data": "trích xuất dữ liệu",
            }
            unique_tools = list(dict.fromkeys(tool_names))
            labels = [tool_label_map.get(t, t.replace("_", " ")) for t in unique_tools[:4]]
            tools_ctx = f"\nCác công cụ đã dùng: {', '.join(labels)}."

        prompt = (
            f"Cuộc trò chuyện:\n"
            f"Người dùng hỏi: {question}\n"
            f"Agent trả lời: {answer}{tools_ctx}\n\n"
            "Hãy đề xuất đúng 3 gợi ý tiếp theo ngắn gọn, thực tế, phù hợp với ngữ cảnh trên.\n"
            "Quy tắc:\n"
            "- Nếu là hành động cụ thể (mở file, chạy lệnh, lưu, xem...) thì bắt đầu bằng '→ '\n"
            "- Nếu là câu hỏi thì viết bình thường\n"
            "- Mỗi gợi ý 1 dòng, tối đa 55 ký tự, tiếng Việt đầy đủ dấu\n"
            "- Không đánh số, không bullet, không giải thích thêm\n"
            "Chỉ trả về 3 dòng gợi ý:"
        )
        r = get_client().messages.create(
            model=mdl,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        text_out = _extract_text_from_content(r.content, "")
        raw = text_out.strip().split("\n")
        lines = [l.strip(" -•–·123456789.) ") for l in raw if l.strip()]
        # Giữ prefix → nếu có
        cleaned = []
        for l in lines:
            if len(l) > 4:
                cleaned.append(l[:70])
        return jsonify({"suggestions": cleaned[:3]})
    except Exception:
        return jsonify({"suggestions": []})


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint — kiểm tra trạng thái server, ChromaDB, scheduler."""
    status = {"ok": True, "ts": datetime.now().isoformat()}
    # Check ChromaDB
    try:
        memory_store.list_memories(limit=1)
        status["chromadb"] = "ok"
    except Exception as e:
        status["chromadb"] = f"error: {e}"
        status["ok"] = False
    # Check scheduler
    status["scheduler"] = "running" if scheduler.running else "stopped"
    status["active_streams"] = len(active_streams)
    status["scheduled_jobs"] = len(scheduled_jobs)
    return jsonify(status), 200 if status["ok"] else 503


@app.after_request
def add_header(response):
    """Vô hiệu hóa cache cho tất cả các file tĩnh để phát triển UI."""
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/shutdown", methods=["POST"])
def shutdown():
    """
    Tắt server khi browser tab đóng.

    Lưu ý: Mặc định **KHÔNG** cho shutdown từ web UI vì dễ làm server "tự tắt" khi người dùng reload/đóng tab.
    Chỉ bật khi chạy bản native (`oculo_app.py`) hoặc khi set OCULO_ALLOW_BROWSER_SHUTDOWN=1.
    """
    if request.remote_addr not in ("127.0.0.1", "::1"):
        return jsonify({"error": "forbidden"}), 403
    allow = (os.getenv("OCULO_ALLOW_BROWSER_SHUTDOWN", "") or "").lower() in ("1", "true", "yes")
    if not allow and _shutdown_callback is None:
        return jsonify({"ok": True, "skipped": True, "reason": "browser_shutdown_disabled"}), 200
    def _kill():
        import time as _t
        _t.sleep(0.3)
        # Gọi callback nếu có (vd. đóng pywebview window)
        cb = _shutdown_callback
        if cb:
            try: cb()
            except Exception: pass
        else:
            os.kill(os.getpid(), 9)
    threading.Thread(target=_kill, daemon=True).start()
    return jsonify({"ok": True})

# Hook để oculo_app.py inject callback đóng window thay vì kill process
_shutdown_callback = None

def set_shutdown_callback(fn):
    global _shutdown_callback
    _shutdown_callback = fn


if __name__ == "__main__":
    print("Oculo: http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)
