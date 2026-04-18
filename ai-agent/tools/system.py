import subprocess
import pyautogui
import PIL.ImageGrab as ImageGrab


def run_applescript(script: str, timeout: int = 15) -> str:
    """Chạy AppleScript để điều khiển macOS apps"""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip() or result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "Error: AppleScript timeout"


def open_app(app_name: str, timeout: int = 10) -> str:
    """Mở một ứng dụng trên macOS"""
    try:
        result = subprocess.run(["open", "-a", app_name], capture_output=True, text=True, timeout=timeout)
        return f"Opened {app_name}" if result.returncode == 0 else result.stderr
    except subprocess.TimeoutExpired:
        return f"Error: timeout opening {app_name}"


def take_screenshot(path: str = "/tmp/screenshot.png") -> str:
    """Chụp màn hình hiện tại"""
    img = ImageGrab.grab()
    img.save(path)
    return path


def click(x: int, y: int):
    """Click chuột tại tọa độ (x, y)"""
    pyautogui.click(x, y)


def type_text(text: str):
    """Gõ văn bản"""
    pyautogui.typewrite(text, interval=0.05)


def run_terminal_command(cmd: str, timeout: int = 30) -> str:
    """Chạy lệnh terminal và trả về output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return f"Error: command timeout after {timeout}s"
