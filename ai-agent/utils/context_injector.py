"""
Context Injector — tự động inject thông tin môi trường vào system prompt.
Thu thập: pwd, apps đang mở, thời gian, màn hình resolution.
Requirements: 3.1 - 3.6
"""
import subprocess
from datetime import datetime


def _run_cmd(cmd: str, timeout: int = 3) -> str:
    """Chạy lệnh shell, trả về output hoặc rỗng nếu lỗi."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip()
    except Exception:
        return ""


def _run_osascript(script: str, timeout: int = 4) -> str:
    """Chạy AppleScript, trả về output hoặc rỗng nếu lỗi."""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip()
    except Exception:
        return ""


def get_environment_context() -> str:
    """
    Thu thập thông tin môi trường song song — tất cả subprocess chạy cùng lúc.
    """
    from concurrent.futures import ThreadPoolExecutor

    def _pwd():
        r = _run_cmd("pwd")
        return f"- Thư mục hiện tại: {r}" if r else ""

    def _time():
        try:
            return f"- Thời gian hiện tại: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        except Exception:
            return ""

    def _apps():
        r = _run_osascript(
            'tell application "System Events" to get name of every process whose background only is false'
        )
        return f"- Ứng dụng đang mở: {r[:300]}" if r else ""

    def _screen():
        r = _run_osascript('tell application "Finder" to get bounds of window of desktop')
        return f"- Màn hình bounds: {r}" if r else ""

    parts = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = [ex.submit(f) for f in [_pwd, _time, _apps, _screen]]
        for f in futures:
            try:
                result = f.result(timeout=5)
                if result:
                    parts.append(result)
            except Exception:
                pass

    if not parts:
        return ""
    return "\n\n[Ngữ cảnh môi trường hiện tại:]\n" + "\n".join(parts)
