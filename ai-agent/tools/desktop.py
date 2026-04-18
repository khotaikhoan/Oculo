import subprocess
import pyautogui
import time
from PIL import ImageGrab

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


def screenshot() -> str:
    path = "/tmp/screen.png"
    ImageGrab.grab().save(path)
    return path


def open_app(app_name: str) -> str:
    # Google Chrome: `open -a` hay mở treo ở màn «Ai sẽ sử dụng Chrome?» — dùng binary + --profile-directory
    an = app_name.strip().lower()
    if an in ("google chrome", "chrome", "chromium", "google chrome.app"):
        try:
            from tools.browser import launch_chrome_gui_without_picker

            return launch_chrome_gui_without_picker()
        except Exception:
            pass
    result = subprocess.run(["open", "-a", app_name], capture_output=True, text=True, timeout=15)
    time.sleep(2)
    return f"Opened {app_name}" if result.returncode == 0 else result.stderr


def run_applescript(script: str) -> str:
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=15)
        return result.stdout.strip() or result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "Error: AppleScript timeout"


def run_shell(cmd: str) -> str:
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=15
    )
    return (result.stdout + result.stderr).strip()


def click(x: int, y: int):
    pyautogui.click(x, y)


def type_text(text: str):
    pyautogui.typewrite(text, interval=0.05)


def hotkey(*keys):
    pyautogui.hotkey(*keys)

def run_shell_streaming(cmd: str, timeout: int = 60):
    """
    Generator: yield từng dòng output từ shell command.
    Yield "__TIMEOUT__" nếu quá thời gian.
    Requirements: 1.1 - 1.5
    """
    import queue
    import threading

    proc = subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1
    )
    q: queue.Queue = queue.Queue()

    def _reader():
        try:
            for line in iter(proc.stdout.readline, ''):
                q.put(line)
        except Exception:
            pass
        finally:
            q.put(None)

    t = threading.Thread(target=_reader, daemon=True)
    t.start()

    import time
    deadline = time.monotonic() + timeout
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                proc.kill()
                yield "__TIMEOUT__"
                return
            try:
                line = q.get(timeout=min(remaining, 1.0))
            except queue.Empty:
                continue
            if line is None:
                break
            yield line.rstrip('\n')
    except Exception as e:
        yield f"__ERROR__: {e}"
    finally:
        try:
            proc.stdout.close()
        except Exception:
            pass
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()
