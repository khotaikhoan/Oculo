"""
Self-Corrector — tự verify kết quả sau khi thực thi tool.
Requirements: 7.1 - 7.5
"""
import logging
from typing import Callable

logger = logging.getLogger(__name__)


def _is_error(s: str) -> bool:
    """Nhận diện chuỗi lỗi từ tool (hỗ trợ cả tiếng Anh và tiếng Việt)."""
    t = (s or "").strip().lower()
    return t.startswith("error") or t.startswith("lỗi:")


def verify_write_file(path: str, expected_content: str, run_tool_fn: Callable) -> dict:
    """
    Xác minh file đã được ghi đúng bằng cách đọc lại.
    """
    try:
        actual = run_tool_fn("read_file", {"path": path})
        if _is_error(actual):
            return {"success": False, "reason": f"read_file failed: {actual}"}
        success = expected_content.strip() in actual or actual.strip() == expected_content.strip()
        return {
            "success": success,
            "expected_len": len(expected_content),
            "actual_len": len(actual),
            "reason": "content match" if success else "content mismatch",
        }
    except Exception as e:
        return {"success": False, "reason": str(e)}


def verify_browser_navigate(url: str, run_tool_fn: Callable) -> dict:
    """
    Xác minh browser đã navigate đúng bằng cách lấy title và URL hiện tại.
    """
    try:
        page_info = run_tool_fn(
            "browser_evaluate",
            {"js": "document.title + ' | ' + window.location.href"}
        )
        if _is_error(page_info):
            return {"success": False, "reason": f"evaluate failed: {page_info}"}
        # Kiểm tra domain có trong URL hiện tại không
        from urllib.parse import urlparse
        expected_domain = urlparse(url).netloc
        success = not _is_error(page_info) and (
            expected_domain in page_info or url in page_info
        )
        return {
            "success": success,
            "page_info": page_info[:200],
            "reason": "navigation confirmed" if success else "domain not found in page",
        }
    except Exception as e:
        return {"success": False, "reason": str(e)}
