"""
Fallback Registry — tách biệt khỏi retry logic.
Retry = thử lại y chang. Fallback = thử cách khác.
"""
import logging
from typing import Callable, Optional

logger = logging.getLogger("oculo.fallback")


class FallbackStrategy:
    def __init__(self, name: str, description: str,
                 transform_input: Optional[Callable] = None):
        self.name = name
        self.description = description
        # transform_input(original_input) → new_input dict | None (None = skip tool)
        self.transform_input = transform_input or (lambda x: x)


# Registry: tool_name → ordered list of FallbackStrategy
FALLBACK_REGISTRY: dict[str, list[FallbackStrategy]] = {

    "browser_click": [
        FallbackStrategy(
            name="browser_evaluate",
            description="Click bằng JavaScript trực tiếp",
            transform_input=lambda inp: {
                "js": (
                    f"(function(){{"
                    f"  var sel = {repr(inp.get('selector',''))};"
                    f"  var txt = {repr(inp.get('text',''))};"
                    f"  var el = sel ? document.querySelector(sel) : null;"
                    f"  if(!el && txt) el = [...document.querySelectorAll('*')]"
                    f"    .find(e => e.textContent.trim() === txt);"
                    f"  if(el) {{ el.click(); return 'clicked'; }}"
                    f"  return 'element not found';"
                    f"}})()"
                )
            },
        ),
        FallbackStrategy(
            name="browser_evaluate",
            description="Tìm element theo text rộng hơn",
            transform_input=lambda inp: {
                "js": (
                    f"(function(){{"
                    f"  var txt = {repr(str(inp.get('text') or inp.get('selector') or '').replace('#','').replace('.',''))};"
                    f"  var el = [...document.querySelectorAll('button,a,input[type=submit],[role=button]')]"
                    f"    .find(e => e.textContent.toLowerCase().includes(txt.toLowerCase()));"
                    f"  if(el) {{ el.click(); return 'clicked via text search'; }}"
                    f"  return 'not found';"
                    f"}})()"
                )
            },
        ),
    ],

    "browser_navigate": [
        FallbackStrategy(
            name="browser_navigate",
            description="Navigate với wait_until=domcontentloaded (nhanh hơn)",
            transform_input=lambda inp: {
                **inp,
                "_fallback_hint": "domcontentloaded",
            },
        ),
        FallbackStrategy(
            name="run_shell",
            description="Lấy nội dung trang qua curl thay vì browser",
            transform_input=lambda inp: {
                "cmd": f"curl -sL --max-time 15 '{inp.get('url','')}' | head -c 5000"
            },
        ),
    ],

    "browser_fill": [
        FallbackStrategy(
            name="browser_evaluate",
            description="Fill input bằng JavaScript",
            transform_input=lambda inp: {
                "js": (
                    f"(function(){{"
                    f"  var el = document.querySelector({repr(inp.get('selector',''))});"
                    f"  if(el) {{"
                    f"    el.focus();"
                    f"    el.value = {repr(inp.get('value',''))};"
                    f"    el.dispatchEvent(new Event('input', {{bubbles:true}}));"
                    f"    el.dispatchEvent(new Event('change', {{bubbles:true}}));"
                    f"    return 'filled';"
                    f"  }}"
                    f"  return 'element not found';"
                    f"}})()"
                )
            },
        ),
    ],

    "screenshot_and_analyze": [
        FallbackStrategy(
            name="browser_evaluate",
            description="Lấy text content thay vì screenshot",
            transform_input=lambda inp: {
                "js": """(function(){
  return JSON.stringify({
    title: document.title,
    url: location.href,
    headings: [...document.querySelectorAll('h1,h2,h3')]
      .slice(0,10).map(h => h.textContent.trim()),
    body_text: document.body.innerText.slice(0, 2000),
    inputs: [...document.querySelectorAll('input,button,textarea,select')]
      .slice(0,15).map(el => ({
        tag: el.tagName, type: el.type||'',
        placeholder: el.placeholder||'',
        text: el.textContent.trim().slice(0,50),
        name: el.name||el.id||''
      })),
    links: [...document.querySelectorAll('a[href]')]
      .slice(0,10).map(a => ({text: a.textContent.trim(), href: a.href}))
  }, null, 2);
})()"""
            },
        ),
    ],

    "run_shell": [
        FallbackStrategy(
            name="run_applescript",
            description="Chạy shell qua AppleScript do shell script",
            transform_input=lambda inp: {
                "script": f'do shell script "{inp.get("cmd","").replace(chr(34), chr(39))}"'
            },
        ),
    ],

    "recall": [
        FallbackStrategy(
            name="recall",
            description="Tìm memory với query ngắn hơn (3 từ đầu)",
            transform_input=lambda inp: {
                **inp,
                "query": " ".join(inp.get("query", "").split()[:3]),
            },
        ),
        FallbackStrategy(
            name="_skip",
            description="Bỏ qua memory recall, tiếp tục task",
            transform_input=lambda inp: None,  # None = skip
        ),
    ],
}


def execute_fallback(
    tool_name: str,
    original_input: dict,
    tool_dispatcher: Callable,
    fallback_index: int = 0,
) -> dict:
    """
    Thực thi fallback strategy theo thứ tự.
    Nếu strategy này fail → tự động thử strategy tiếp theo.

    Returns:
        {"success": bool, "result": str, "fallback_used": str,
         "skipped": bool, "exhausted": bool}
    """
    strategies = FALLBACK_REGISTRY.get(tool_name, [])

    if fallback_index >= len(strategies):
        return {
            "success": False,
            "result": f"Không còn fallback nào cho {tool_name}",
            "exhausted": True,
            "skipped": False,
            "fallback_used": None,
        }

    strategy = strategies[fallback_index]
    new_input = strategy.transform_input(original_input)

    logger.info(
        f"Fallback {fallback_index + 1}/{len(strategies)} for {tool_name}: "
        f"{strategy.name} — {strategy.description}"
    )

    # None input = skip tool
    if new_input is None:
        return {
            "success": True,
            "result": f"Đã bỏ qua {tool_name} (fallback: skip)",
            "skipped": True,
            "exhausted": False,
            "fallback_used": strategy.name,
        }

    # _skip là sentinel name
    if strategy.name == "_skip":
        return {
            "success": True,
            "result": f"Đã bỏ qua {tool_name}",
            "skipped": True,
            "exhausted": False,
            "fallback_used": "_skip",
        }

    try:
        result = tool_dispatcher(strategy.name, new_input)
        if isinstance(result, str) and (
            result.startswith("Error:") or result.startswith("Lỗi:")
        ):
            raise RuntimeError(result)

        return {
            "success": True,
            "result": result,
            "skipped": False,
            "exhausted": False,
            "fallback_used": strategy.name,
            "description": strategy.description,
        }
    except Exception as exc:
        logger.warning(f"Fallback {strategy.name} also failed: {exc}")
        # Thử strategy tiếp theo
        return execute_fallback(
            tool_name, original_input, tool_dispatcher, fallback_index + 1
        )
