"""Phân tích lỗi tool và đề xuất cách khắc phục, kèm fallback action thực tế."""
import os
import re
import shlex
from dotenv import load_dotenv
load_dotenv()

HAIKU_MODEL = os.getenv("HAIKU_MODEL") or os.getenv("MODEL", "claude-sonnet-4-5")

RECOVERY_HINTS = {
    "run_shell": "Thử lệnh khác, kiểm tra syntax, hoặc dùng đường dẫn tuyệt đối",
    "browser_navigate": "Kiểm tra URL, thử lại sau 2s, hoặc dùng curl thay thế",
    "browser_click": "Thử selector khác, scroll đến element, hoặc dùng JavaScript click",
    "browser_fill": "Thử click vào field trước, kiểm tra selector, hoặc dùng evaluate",
    "read_file": "Kiểm tra đường dẫn file, thử expanduser, kiểm tra permissions",
    "write_file": "Kiểm tra thư mục tồn tại, thử tạo thư mục trước",
}

# Fallback actions: (tool_name, error_pattern) → (fallback_tool, fallback_input_fn)
def _browser_navigate_fallback(inputs: dict) -> dict | None:
    """Khi browser_navigate fail, thử curl để lấy nội dung."""
    url = inputs.get("url", "")
    if url and url.startswith("http"):
        safe_url = shlex.quote(url)
        return {"tool": "run_shell", "inputs": {"cmd": f"curl -sL --max-time 10 {safe_url} | head -c 3000"}}
    return None


def _run_shell_fallback(inputs: dict) -> dict | None:
    """Khi run_shell fail với lệnh có file path tương đối (./... hoặc ../...), thử với đường dẫn tuyệt đối."""
    cmd = inputs.get("cmd", "")
    if cmd and (cmd.startswith("./") or cmd.startswith("../")):
        return {"tool": "run_shell", "inputs": {"cmd": f"cd $HOME && {cmd}"}}
    return None


FALLBACK_ACTIONS = {
    "browser_navigate": _browser_navigate_fallback,
    "run_shell": _run_shell_fallback,
}

NON_RECOVERABLE_PATTERNS = [
    "permission denied", "not found", "no such file",
    "syntax error", "command not found", "operation not permitted",
]


def get_recovery_suggestion(tool_name: str, error: str, inputs: dict) -> str:
    """Trả về gợi ý recovery ngắn gọn."""
    hint = RECOVERY_HINTS.get(tool_name, "Thử cách tiếp cận khác")
    return f"Tool {tool_name} thất bại: {error[:200]}. Gợi ý: {hint}"


def get_fallback_action(tool_name: str, error: str, inputs: dict) -> dict | None:
    """
    Trả về fallback action nếu có: {"tool": str, "inputs": dict}
    Trả về None nếu không có fallback phù hợp.
    """
    if not is_recoverable(error):
        return None
    fn = FALLBACK_ACTIONS.get(tool_name)
    if fn:
        return fn(inputs)
    return None


def is_recoverable(error: str) -> bool:
    """Kiểm tra lỗi có thể recover không."""
    error_lower = error.lower()
    return not any(p in error_lower for p in NON_RECOVERABLE_PATTERNS)
