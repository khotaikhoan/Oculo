"""
Computer Use controller using Anthropic's computer-use tool.
Agent sees the screen and controls mouse/keyboard directly.

Background use (macOS): while the agent runs, optional `caffeinate` keeps the
system from idle-sleeping so you can switch apps or step away without the
session freezing mid-task. This does not replace a logged-in session: the screen
must not be locked, and vision+GUI automation cannot run truly headless.
"""
import base64
import json
import os
import platform
import subprocess
import threading
import pyautogui
import time
from PIL import ImageGrab
import anthropic
from dotenv import load_dotenv

load_dotenv()

# Dùng model từ env, fallback về claude-sonnet-4.6
MODEL = os.getenv("MODEL", "claude-sonnet-4.6")
SCREEN_W, SCREEN_H = pyautogui.size()
# Timeout cho mỗi API call — tránh treo vô thời hạn
_API_TIMEOUT_SEC = float(os.getenv("COMPUTER_USE_API_TIMEOUT", "45") or 45)


def _check_macos_permissions() -> str | None:
    """Trả về message lỗi nếu macOS thiếu permission cần thiết, None nếu OK."""
    if platform.system() != "Darwin":
        return None
    try:
        img = ImageGrab.grab(bbox=(0, 0, 2, 2))
        if img is None or img.size == (0, 0):
            return (
                "Chưa được cấp quyền Screen Recording. "
                "Mở System Settings → Privacy & Security → Screen Recording → bật cho Oculo/Terminal, "
                "sau đó khởi động lại app."
            )
    except Exception as e:
        return (
            "Không chụp được màn hình (có thể thiếu quyền Screen Recording). "
            f"Chi tiết: {e}"
        )
    try:
        pyautogui.position()
    except Exception as e:
        return (
            "Không đọc được vị trí chuột (có thể thiếu quyền Accessibility). "
            "Mở System Settings → Privacy & Security → Accessibility → bật cho Oculo/Terminal. "
            f"Chi tiết: {e}"
        )
    return None


def _clamp_coord(x, y) -> tuple[int, int]:
    """Clamp (x,y) vào màn hình thực tế; raise ValueError nếu lệch quá xa."""
    try:
        ix, iy = int(x), int(y)
    except Exception as exc:
        raise ValueError(f"Tọa độ không hợp lệ: ({x}, {y}) — {exc}")
    # Cho phép lệch nhẹ (padding) nhưng chặn giá trị hoàn toàn sai
    pad = 50
    if ix < -pad or iy < -pad or ix > SCREEN_W + pad or iy > SCREEN_H + pad:
        raise ValueError(
            f"Tọa độ ({ix}, {iy}) nằm ngoài màn hình {SCREEN_W}x{SCREEN_H}. "
            "Vision có thể đang đoán sai — hãy chụp lại màn hình."
        )
    return max(0, min(ix, SCREEN_W - 1)), max(0, min(iy, SCREEN_H - 1))


def _caffeinate_popen():
    """Giữ máy không vào idle sleep trong lúc agent chạy — bạn có thể đổi sang app khác."""
    if platform.system() != "Darwin":
        return None
    if os.getenv("COMPUTER_USE_CAFFEINATE", "1").lower() not in ("1", "true", "yes"):
        return None
    args = ["caffeinate", "-i"]
    if os.getenv("COMPUTER_USE_KEEP_DISPLAY_AWAKE", "").lower() in ("1", "true", "yes"):
        args.insert(1, "-d")
    try:
        return subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception:
        return None


def _terminate_caffeinate(proc: subprocess.Popen | None):
    if not proc or proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()


def take_screenshot() -> str:
    """Take screenshot and return base64."""
    import tempfile
    path = tempfile.mktemp(suffix=".png", prefix="cu_screen_")
    img = ImageGrab.grab()
    # Scale down if too large (API limit)
    max_w = 1280
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)))
    img.save(path)
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode()


def _truncate_for_log(text: str, limit: int = 50) -> str:
    s = str(text or "")
    return s if len(s) <= limit else s[:limit] + "…"


def execute_action(action: dict) -> str:
    """Execute a computer use action.
    Supports both 'type' (legacy) and 'action' (Anthropic computer-use-2024-10-22 API) keys.
    """
    atype = action.get("action") or action.get("type")
    try:
        if atype == "screenshot":
            return "screenshot_taken"

        elif atype == "mouse_move":
            x, y = _clamp_coord(*action["coordinate"])
            pyautogui.moveTo(x, y, duration=0.3)
            return f"Moved to ({x}, {y})"

        elif atype == "left_click":
            x, y = _clamp_coord(*action["coordinate"])
            pyautogui.click(x, y)
            time.sleep(0.3)
            return f"Clicked ({x}, {y})"

        elif atype == "right_click":
            x, y = _clamp_coord(*action["coordinate"])
            pyautogui.rightClick(x, y)
            return f"Right-clicked ({x}, {y})"

        elif atype == "double_click":
            x, y = _clamp_coord(*action["coordinate"])
            pyautogui.doubleClick(x, y)
            return f"Double-clicked ({x}, {y})"

        elif atype == "left_click_drag":
            sx, sy = _clamp_coord(*action.get("start_coordinate", action.get("coordinate", [0, 0])))
            ex, ey = _clamp_coord(*action.get("coordinate", [sx, sy]))
            pyautogui.moveTo(sx, sy)
            pyautogui.dragTo(ex, ey, duration=0.4, button='left')
            return f"Dragged ({sx},{sy}) → ({ex},{ey})"

        elif atype == "type":
            text = action.get("text", "")
            # Use pyperclip + paste for Unicode/Vietnamese support
            try:
                import pyperclip
                pyperclip.copy(text)
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "v")
                else:
                    pyautogui.hotkey("ctrl", "v")
            except Exception:
                pyautogui.typewrite(text, interval=0.04)
            return f"Typed: {_truncate_for_log(text)}"

        elif atype == "key":
            _is_mac = platform.system() == "Darwin"
            key = action.get("text", "")
            key_map = {
                "Return": "enter", "BackSpace": "backspace",
                "Tab": "tab", "Escape": "escape",
                "ctrl+c": "command+c" if _is_mac else "ctrl+c",
                "ctrl+v": "command+v" if _is_mac else "ctrl+v",
                "ctrl+a": "command+a" if _is_mac else "ctrl+a",
                "ctrl+z": "command+z" if _is_mac else "ctrl+z",
                "ctrl+x": "command+x" if _is_mac else "ctrl+x",
                "cmd+c": "command+c",
                "cmd+v": "command+v",
                "cmd+a": "command+a",
                "super": "command", "Delete": "delete",
                "Home": "home", "End": "end",
                "Page_Up": "pageup", "Page_Down": "pagedown",
            }
            mapped = key_map.get(key, key)
            if "+" in mapped:
                parts = mapped.split("+")
                pyautogui.hotkey(*parts)
            else:
                pyautogui.press(mapped)
            return f"Key: {key}"

        elif atype == "scroll":
            x, y = _clamp_coord(*action["coordinate"])
            direction = action.get("direction", "down")
            amount = action.get("amount", 3)
            pyautogui.moveTo(x, y)
            pyautogui.scroll(-amount if direction == "down" else amount)
            return f"Scrolled {direction} at ({x}, {y})"

        elif atype == "wait":
            duration = min(action.get("duration", 1), 5)
            time.sleep(duration)
            return f"Waited {duration}s"

        return f"Unknown action: {atype}"
    except ValueError as ve:
        # Bounds error — trả rõ ràng cho agent biết để tự sửa
        return f"Action error ({atype}): {ve}"
    except Exception as e:
        return f"Action error ({atype}): {e}"


def run_computer_use(task: str, client: anthropic.Anthropic, max_steps: int = 20,
                     abort_event: threading.Event | None = None):
    """
    Run computer use agent. Generator yielding step events.
    Pass abort_event to support mid-task cancellation.
    """
    # Kiểm tra permission macOS trước khi bắt đầu — báo lỗi rõ ràng
    perm_err = _check_macos_permissions()
    if perm_err:
        yield {"type": "error", "content": perm_err}
        return

    # Computer use tool definition
    computer_tool = {
        "type": "computer_20241022",
        "name": "computer",
        "display_width_px": SCREEN_W,
        "display_height_px": SCREEN_H,
        "display_number": 1,
    }

    system = f"""You are controlling a macOS computer. Screen resolution: {SCREEN_W}x{SCREEN_H}.
The user may switch to another app or not watch the screen; keep working until the task is done.
Use the computer tool to complete the task. Take a screenshot first to see the current state.
Be precise with coordinates. After each action, take a screenshot to verify the result.
IMPORTANT: You are controlling the actual macOS desktop, NOT a web browser UI.
Ignore any web browser showing an AI Agent interface - focus only on completing the given task."""

    messages = [{"role": "user", "content": task}]
    steps = 0

    def _aborted() -> bool:
        return bool(abort_event and abort_event.is_set())

    caf = _caffeinate_popen()
    try:
        while steps < max_steps:
            if _aborted():
                yield {"type": "interrupted", "content": "Đã dừng theo yêu cầu người dùng."}
                return
            steps += 1
            yield {"type": "progress", "step": steps, "max_steps": max_steps}

            screenshot_b64 = take_screenshot()

            if messages[-1]["role"] == "user" and isinstance(messages[-1]["content"], str):
                messages[-1]["content"] = [
                    {"type": "text", "text": messages[-1]["content"]},
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": screenshot_b64}}
                ]

            try:
                response = client.beta.messages.create(
                    model=MODEL,
                    max_tokens=1024,
                    system=system,
                    tools=[computer_tool],
                    messages=messages,
                    betas=["computer-use-2024-10-22"],
                    timeout=_API_TIMEOUT_SEC,
                )
            except anthropic.APITimeoutError:
                yield {"type": "error", "content": f"Model timeout (>{int(_API_TIMEOUT_SEC)}s). Thử lại hoặc rút gọn task."}
                return
            except Exception as e:
                yield {"type": "error", "content": str(e)}
                return

            if _aborted():
                yield {"type": "interrupted", "content": "Đã dừng theo yêu cầu người dùng."}
                return

            text_out = ""
            for block in response.content:
                if hasattr(block, "text") and block.text:
                    text_out += block.text

            if text_out:
                yield {"type": "text", "content": text_out}

            if response.stop_reason == "end_turn":
                yield {"type": "done", "content": text_out or "Task completed."}
                return

            serialized = []
            for b in response.content:
                if hasattr(b, "text"):
                    serialized.append({"type": "text", "text": b.text})
                elif b.type == "tool_use":
                    serialized.append({"type": "tool_use", "id": b.id, "name": b.name, "input": b.input})
            messages.append({"role": "assistant", "content": serialized})

            tool_results = []
            for block in response.content:
                if block.type != "tool_use" or block.name != "computer":
                    continue
                if _aborted():
                    yield {"type": "interrupted", "content": "Đã dừng theo yêu cầu người dùng."}
                    return

                action = block.input
                yield {"type": "action", "action": action}

                result = execute_action(action)
                time.sleep(0.4)

                # Chỉ chụp sau action thực sự thay đổi màn hình (bỏ qua screenshot/wait)
                atype = action.get("action") or action.get("type")
                skip_post_screenshot = atype in ("screenshot", "wait")
                if skip_post_screenshot:
                    # Reuse frame mới nhất để tiết kiệm chi phí
                    new_screenshot = screenshot_b64
                else:
                    new_screenshot = take_screenshot()
                    yield {"type": "screenshot", "data": new_screenshot}

                tool_result_content = [{"type": "text", "text": result}]
                if atype != "screenshot":
                    tool_result_content.append({
                        "type": "image",
                        "source": {"type": "base64", "media_type": "image/png", "data": new_screenshot}
                    })

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": tool_result_content
                })

            if tool_results:
                messages.append({"role": "user", "content": tool_results})

        yield {"type": "done", "content": f"Reached max steps ({max_steps})."}
    finally:
        _terminate_caffeinate(caf)
