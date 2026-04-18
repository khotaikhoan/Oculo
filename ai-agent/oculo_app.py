"""
Oculo App — Flask server + pywebview native window
Chạy: python3 oculo_app.py

Khi đóng gói bằng PyInstaller (dist/Oculo.app), bundle là read-only:
- `.env` của người dùng lưu ở ~/Library/Application Support/Oculo/.env
- Log ghi vào Application Support để hỗ trợ gỡ rối khi app không mở
- sys.path thêm sys._MEIPASS (nơi PyInstaller giải nén) để import được submodules
"""
import os
import sys
import threading
import time
import signal
import traceback

# Khi frozen, module đi kèm được giải nén vào sys._MEIPASS; khi dev, đứng cạnh file này.
_HERE = os.path.dirname(os.path.abspath(__file__))
_MEIPASS = getattr(sys, "_MEIPASS", None)
for _p in (_MEIPASS, _HERE):
    if _p and _p not in sys.path:
        sys.path.insert(0, _p)

from utils.app_paths import app_support_dir, dotenv_path, is_frozen  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

# Nạp .env từ Application Support trước khi import server — key_manager đọc
# env ở import time.
load_dotenv(dotenv_path())

os.environ.setdefault("PORT", "8080")
PORT = int(os.getenv("PORT", 8080))

# Ghi log khởi động ra file để gỡ lỗi khi người dùng cài từ .dmg: nếu app không
# mở được thì mở ~/Library/Application Support/Oculo/launch.log để xem lý do.
_LOG_PATH = app_support_dir() / "launch.log"
try:
    _log_fh = open(_LOG_PATH, "a", buffering=1, encoding="utf-8")
    if is_frozen():
        sys.stdout = _log_fh
        sys.stderr = _log_fh
except Exception:
    _log_fh = None


def _log(msg: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)


_log(f"Oculo khởi động (frozen={is_frozen()}, PORT={PORT}, MEIPASS={_MEIPASS})")

# ── 1. Khởi động Flask trong thread riêng ──
_server_ready = threading.Event()
_server_error: list[BaseException] = []


def _start_flask():
    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    try:
        from server import app as flask_app
        _server_ready.set()
        flask_app.run(
            host="127.0.0.1",
            port=PORT,
            debug=False,
            threaded=True,
            use_reloader=False,
        )
    except BaseException as exc:  # noqa: BLE001
        _server_error.append(exc)
        _log("Flask thread crash:\n" + "".join(traceback.format_exception(exc)))
        _server_ready.set()  # unblock cửa sổ để hiện trang lỗi


flask_thread = threading.Thread(target=_start_flask, daemon=True)
flask_thread.start()

# ── 2. Đợi server bind port ──
_log("Đợi server khởi động...")
_server_ready.wait(timeout=30)

if _server_error:
    _log("Server không khởi động được — xem stack ở trên. Thoát.")
    # Vẫn cố mở một cửa sổ báo lỗi để user không bị 'bounce' im lặng trong Dock.

for _ in range(60):
    try:
        import urllib.request
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}", timeout=1)
        _log("Server đã phản hồi cổng 8080.")
        break
    except Exception:
        time.sleep(0.5)
else:
    _log("Server chưa phản hồi sau 30s. Vẫn thử mở cửa sổ để báo lỗi.")


def _error_html(err_text: str) -> str:
    esc = (
        err_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    return (
        "<!doctype html><meta charset='utf-8'>"
        "<title>Oculo — lỗi khởi động</title>"
        "<style>body{font:14px/1.5 -apple-system,system-ui,sans-serif;"
        "padding:24px;color:#eee;background:#1d1f23}h1{font-size:18px}"
        "pre{background:#111;padding:12px;border-radius:8px;overflow:auto;"
        "max-height:60vh;white-space:pre-wrap}</style>"
        "<h1>Oculo không thể khởi động server.</h1>"
        f"<p>Log: <code>{_LOG_PATH}</code></p><pre>{esc}</pre>"
    )


# ── 3. Mở cửa sổ pywebview ──
try:
    import webview

    if _server_error:
        err_text = "".join(traceback.format_exception(_server_error[0]))
        window = webview.create_window(
            title="Oculo — Lỗi",
            html=_error_html(err_text),
            width=900,
            height=600,
        )
    else:
        from server import set_shutdown_callback  # type: ignore

        window = webview.create_window(
            title="Oculo",
            url=f"http://127.0.0.1:{PORT}",
            width=1280,
            height=860,
            min_size=(900, 600),
            resizable=True,
            text_select=True,
            zoomable=True,
        )

        def _close_window():
            try:
                window.destroy()
            except Exception:
                pass

        set_shutdown_callback(_close_window)

    def _on_closed():
        os.kill(os.getpid(), signal.SIGTERM)

    window.events.closed += _on_closed

    webview.start(debug=False, private_mode=False)

except ImportError:
    import webbrowser
    webbrowser.open(f"http://127.0.0.1:{PORT}")
    _log("pywebview không có, đã mở trình duyệt. Ctrl+C để tắt.")
    try:
        signal.pause()
    except AttributeError:
        while True:
            time.sleep(60)
