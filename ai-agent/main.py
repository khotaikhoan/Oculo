"""
AI Agent - dùng Anthropic Claude trực tiếp (không cần open-interpreter)
"""

import os
import json
import anthropic
from dotenv import load_dotenv
from tools import desktop, browser

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
)
MODEL = os.getenv("MODEL", "claude-sonnet-4.6")

# Định nghĩa tools cho Claude
TOOLS = [
    {
        "name": "run_shell",
        "description": "Chạy lệnh terminal/bash trên macOS",
        "input_schema": {
            "type": "object",
            "properties": {"cmd": {"type": "string", "description": "Lệnh shell cần chạy"}},
            "required": ["cmd"]
        }
    },
    {
        "name": "open_app",
        "description": "Mở một ứng dụng trên macOS",
        "input_schema": {
            "type": "object",
            "properties": {"app_name": {"type": "string", "description": "Tên app, ví dụ: Safari, Finder, Mail"}},
            "required": ["app_name"]
        }
    },
    {
        "name": "run_applescript",
        "description": "Chạy AppleScript để điều khiển macOS apps",
        "input_schema": {
            "type": "object",
            "properties": {"script": {"type": "string", "description": "AppleScript code"}},
            "required": ["script"]
        }
    },
    {
        "name": "browser_navigate",
        "description": "Mở URL trong Chromium browser",
        "input_schema": {
            "type": "object",
            "properties": {"url": {"type": "string", "description": "URL cần mở"}},
            "required": ["url"]
        }
    },
    {
        "name": "browser_get_text",
        "description": "Lấy nội dung text của trang web hiện tại",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "browser_get_element_text",
        "description": "Lấy text của một element cụ thể theo CSS selector",
        "input_schema": {
            "type": "object",
            "properties": {"selector": {"type": "string", "description": "CSS selector"}},
            "required": ["selector"]
        }
    },
    {
        "name": "browser_get_title",
        "description": "Lấy tiêu đề trang web hiện tại",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "browser_fill",
        "description": "Điền text vào input (sensitive=true cho mật khẩu)",
        "input_schema": {
            "type": "object",
            "properties": {
                "selector": {"type": "string", "description": "CSS selector của input"},
                "value": {"type": "string", "description": "Giá trị cần điền"},
                "sensitive": {"type": "boolean"},
            },
            "required": ["selector", "value"]
        }
    },
    {
        "name": "browser_click",
        "description": "Click vào element (selector hoặc text hiển thị)",
        "input_schema": {
            "type": "object",
            "properties": {
                "selector": {"type": "string"},
                "text": {"type": "string"},
            },
            "required": []
        }
    },
    {
        "name": "browser_scroll",
        "description": "Cuộn trang tự nhiên (lên/xuống)",
        "input_schema": {
            "type": "object",
            "properties": {
                "direction": {"type": "string"},
                "amount": {},
                "selector": {"type": "string"},
            },
            "required": []
        }
    },
    {
        "name": "browser_wait_for_human",
        "description": "Đợi network/selector với khoảng polling tự nhiên",
        "input_schema": {
            "type": "object",
            "properties": {
                "condition": {"type": "string"},
                "timeout_ms": {"type": "integer"},
            },
            "required": ["condition"]
        }
    },
    {
        "name": "browser_evaluate",
        "description": "Chạy JavaScript trên trang web để lấy dữ liệu nhanh. Ví dụ: document.querySelector('.weather').innerText",
        "input_schema": {
            "type": "object",
            "properties": {"js": {"type": "string", "description": "JavaScript expression"}},
            "required": ["js"]
        }
    },
    {
        "name": "screenshot",
        "description": "Chụp màn hình desktop để quan sát trạng thái",
        "input_schema": {"type": "object", "properties": {}}
    }
]

SYSTEM = """Bạn là AI Agent chạy trên macOS. Bạn có thể điều khiển máy tính thông qua các tools.

Khi trả lời hoặc điền chuỗi tiếng Việt (kể cả trong tham số tool): luôn dùng tiếng Việt chuẩn, đầy đủ dấu thanh và dấu mũ; không viết không dấu trừ khi người dùng yêu cầu.

Khi nhận yêu cầu:
1. Phân tích cần làm gì
2. Gọi tool phù hợp từng bước
3. Để lấy thời tiết: dùng run_shell với curl thay vì browser vì nhanh hơn:
   - curl -s "https://wttr.in/Hanoi?format=3" để lấy thời tiết ngắn gọn
   - curl -s "https://wttr.in/Hanoi?format=%l:+%C+%t+%h+%w" để lấy chi tiết
4. Với web thông thường: dùng browser_navigate rồi browser_evaluate với: document.body.innerText.substring(0,2000)
5. Báo cáo kết quả CỤ THỂ bằng tiếng Việt - phải có số liệu/nội dung thực tế

KHÔNG báo cáo chung chung. Phải có dữ liệu thực."""


def run_tool(name: str, inputs: dict) -> str:
    try:
        if name == "run_shell":
            return desktop.run_shell(inputs["cmd"])
        elif name == "open_app":
            return desktop.open_app(inputs["app_name"])
        elif name == "run_applescript":
            return desktop.run_applescript(inputs["script"])
        elif name == "browser_navigate":
            return browser.navigate(inputs["url"])
        elif name == "browser_get_text":
            return browser.get_text()
        elif name == "browser_get_element_text":
            return browser.get_element_text(inputs["selector"])
        elif name == "browser_get_title":
            return browser.get_page_title()
        elif name == "browser_evaluate":
            return browser.evaluate(inputs["js"])
        elif name == "browser_fill":
            return browser.fill(
                inputs["selector"],
                inputs["value"],
                sensitive=bool(inputs.get("sensitive", False)),
            )
        elif name == "browser_click":
            return browser.click_selector(
                inputs.get("selector") or None,
                inputs.get("text") or None,
            )
        elif name == "browser_scroll":
            return browser.browser_scroll(
                inputs.get("direction", "down"),
                inputs.get("amount", "medium"),
                inputs.get("selector"),
            )
        elif name == "browser_wait_for_human":
            return browser.browser_wait_for_human(
                inputs["condition"],
                int(inputs.get("timeout_ms", 10000)),
            )
        elif name == "screenshot":
            path = desktop.screenshot()
            return f"Screenshot saved: {path}"
        else:
            return f"Unknown tool: {name}"
    except Exception as e:
        return f"Error: {e}"


def chat(user_message: str):
    messages = [{"role": "user", "content": user_message}]
    print(f"\nAgent đang xử lý...\n")

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages
        )

        # In text response nếu có
        for block in response.content:
            if hasattr(block, "text"):
                print(f"Agent: {block.text}")

        # Nếu không còn tool call thì dừng
        if response.stop_reason != "tool_use":
            break

        # Xử lý tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  → Gọi tool: {block.name}({json.dumps(block.input, ensure_ascii=False)})")
                result = run_tool(block.name, block.input)
                print(f"  ← Kết quả: {result[:200]}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        # Thêm response và tool results vào messages
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})


def main():
    print("=" * 50)
    print("AI Agent sẵn sàng. Gõ 'exit' để thoát.")
    print("=" * 50)
    while True:
        try:
            user_input = input("\nBạn: ").strip()
            if user_input.lower() in ("exit", "quit", "thoát"):
                break
            if user_input:
                chat(user_input)
        except KeyboardInterrupt:
            break
    print("\nTạm biệt!")


if __name__ == "__main__":
    main()
