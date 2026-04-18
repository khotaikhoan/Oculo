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
import pyautogui
import time
from PIL import ImageGrab
import anthropic
from dotenv import load_dotenv

load_dotenv()

# Dùng model từ env, fallback về claude-sonnet-4.6
MODEL = os.getenv("MODEL", "claude-sonnet-4.6")
SCREEN_W, SCREEN_H = pyautogui.size()


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


def execute_action(action: dict) -> str:
    """Execute a computer use action.
    Supports both 'type' (legacy) and 'action' (Anthropic computer-use-2024-10-22 API) keys.
    """
    atype = action.get("action") or action.get("type")
    try:
        if atype == "screenshot":
            return "screenshot_taken"

        elif atype == "mouse_move":
            x, y = action["coordinate"]
            pyautogui.moveTo(x, y, duration=0.3)
            return f"Moved to ({x}, {y})"

        elif atype == "left_click":
            x, y = action["coordinate"]
            pyautogui.click(x, y)
            time.sleep(0.3)
            return f"Clicked ({x}, {y})"

        elif atype == "right_click":
            x, y = action["coordinate"]
            pyautogui.rightClick(x, y)
            return f"Right-clicked ({x}, {y})"

        elif atype == "double_click":
            x, y = action["coordinate"]
            pyautogui.doubleClick(x, y)
            return f"Double-clicked ({x}, {y})"

        elif atype == "left_click_drag":
            sx, sy = action.get("start_coordinate", action.get("coordinate", [0, 0]))
            ex, ey = action.get("coordinate", [sx, sy])
            pyautogui.moveTo(sx, sy)
            pyautogui.dragTo(ex, ey, duration=0.4, button='left')
            return f"Dragged ({sx},{sy}) → ({ex},{ey})"

        elif atype == "type":
            text = action.get("text", "")
            # Use pyperclip + paste for Unicode/Vietnamese support
            try:
                import pyperclip
                pyperclip.copy(text)
                import platform
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "v")
                else:
                    pyautogui.hotkey("ctrl", "v")
            except Exception:
                pyautogui.typewrite(text, interval=0.04)
            return f"Typed: {text[:50]}"

        elif atype == "key":
            import platform
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
            x, y = action["coordinate"]
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
    except Exception as e:
        return f"Action error ({atype}): {e}"


def run_computer_use(task: str, client: anthropic.Anthropic, max_steps: int = 20):
    """
    Run computer use agent. Generator yielding step events.
    """
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

    caf = _caffeinate_popen()
    try:
        while steps < max_steps:
            steps += 1

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
                )
            except Exception as e:
                yield {"type": "error", "content": str(e)}
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

                action = block.input
                yield {"type": "action", "action": action}

                result = execute_action(action)
                time.sleep(0.4)

                new_screenshot = take_screenshot()
                yield {"type": "screenshot", "data": new_screenshot}

                tool_result_content = [{"type": "text", "text": result}]
                if action.get("action") != "screenshot" and action.get("type") != "screenshot":
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
