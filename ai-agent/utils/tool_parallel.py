"""
Tool Parallelism — chạy các tool calls độc lập song song với ThreadPoolExecutor.
Requirements: 9.1 - 9.6
"""
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

logger = logging.getLogger(__name__)

# Các tool có thể chạy song song (không có side effects lẫn nhau)
INDEPENDENT_TOOLS = {
    # System / file / shell
    "run_shell", "read_file", "recall", "notify",
    # Screenshot (read-only)
    "screenshot_and_analyze",
    # Browser DOM reads — không mutate state
    "browser_evaluate",
    "browser_get_text",
    "browser_get_title",
    "browser_list_tabs",
    "browser_get_dom_state",
    "browser_get_page_state",
    "browser_get_conv_context",
    "browser_macro_list",
    # Preflight check — curl HEAD, không mở page
    "browser_preflight_check",
    # Memory
    "remember",
    "extract_data",
}
MAX_WORKERS = 5


def can_run_parallel(tool_blocks: list) -> bool:
    """Kiểm tra xem các tool calls có thể chạy song song không."""
    if len(tool_blocks) <= 1:
        return False
    return all(b.name in INDEPENDENT_TOOLS for b in tool_blocks)


def run_tools_parallel(
    tool_blocks: list,
    run_tool_fn: Callable,
    max_workers: int = MAX_WORKERS,
) -> list[dict]:
    """
    Chạy tool calls song song.
    Returns: list of {"tool_use_id": ..., "result": ..., "name": ...}
    """
    results = [None] * len(tool_blocks)

    def execute_one(idx: int, block):
        try:
            result = run_tool_fn(block.name, block.input)
            return idx, result
        except Exception as e:
            return idx, f"Error: {e}"

    workers = min(len(tool_blocks), max_workers)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(execute_one, i, block): i
            for i, block in enumerate(tool_blocks)
        }
        for future in as_completed(futures):
            try:
                idx, result = future.result()
                results[idx] = {
                    "tool_use_id": tool_blocks[idx].id,
                    "name": tool_blocks[idx].name,
                    "result": result,
                }
            except Exception as e:
                orig_idx = futures[future]
                results[orig_idx] = {
                    "tool_use_id": tool_blocks[orig_idx].id,
                    "name": tool_blocks[orig_idx].name,
                    "result": f"Error: {e}",
                }

    return results
