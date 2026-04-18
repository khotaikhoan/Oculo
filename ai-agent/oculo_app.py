"""
Oculo App — Flask server + pywebview native window
Chạy: python3 oculo_app.py
"""
import os, sys, threading, time, signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("PORT", "8080")

from dotenv import load_dotenv
load_dotenv()

PORT = int(os.getenv("PORT", 8080))

# ── 1. Khởi động Flask trong thread riêng ──
_server_ready = threading.Event()

def _start_flask():
    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    from server import app as flask_app
    _server_ready.set()
    flask_app.run(host="127.0.0.1", port=PORT,
                  debug=False, threaded=True, use_reloader=False)

flask_thread = threading.Thread(target=_start_flask, daemon=True)
flask_thread.start()

# ── 2. Đợi server bind port ──
print("Đợi server khởi động...")
_server_ready.wait(timeout=20)

for _ in range(40):
    try:
        import urllib.request
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}", timeout=1)
        break
    except Exception:
        time.sleep(0.5)

print(f"Server sẵn sàng tại http://127.0.0.1:{PORT}")

# ── 3. Mở cửa sổ pywebview ──
try:
    import webview
    from server import set_shutdown_callback

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
        try: window.destroy()
        except Exception: pass

    # Khi tab gọi /shutdown → đóng cửa sổ
    set_shutdown_callback(_close_window)

    # Khi đóng cửa sổ → tắt toàn bộ process
    def _on_closed():
        os.kill(os.getpid(), signal.SIGTERM)

    window.events.closed += _on_closed

    webview.start(debug=False, private_mode=False)

except ImportError:
    import webbrowser
    webbrowser.open(f"http://127.0.0.1:{PORT}")
    print("pywebview không có, đã mở Chrome. Ctrl+C để tắt.")
    try:
        signal.pause()
    except AttributeError:
        while True: time.sleep(60)
