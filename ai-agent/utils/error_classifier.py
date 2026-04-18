"""
Error Classification System — phân loại lỗi 3 tầng:
  Transient  → tự khỏi, retry được
  Recoverable → cần đổi cách, có fallback
  Fatal      → abort ngay, báo user
"""
import re
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class ErrorCategory(Enum):
    # Transient — retry được
    TRANSIENT_NETWORK    = "transient_network"
    TRANSIENT_RATE_LIMIT = "transient_rate_limit"
    TRANSIENT_OVERLOAD   = "transient_overload"
    TRANSIENT_LOCK       = "transient_lock"
    TRANSIENT_RENDERING  = "transient_rendering"

    # Recoverable — cần fallback
    RECOVERABLE_ELEMENT_NOT_FOUND = "recoverable_element"
    RECOVERABLE_NAVIGATION_FAILED = "recoverable_navigation"
    RECOVERABLE_AUTH_EXPIRED      = "recoverable_auth"
    RECOVERABLE_CONTENT_CHANGED   = "recoverable_content"
    RECOVERABLE_TOOL_WRONG_PARAMS = "recoverable_params"

    # Fatal — abort ngay
    FATAL_PERMISSION_DENIED = "fatal_permission"
    FATAL_FILE_NOT_EXIST    = "fatal_file_not_exist"
    FATAL_INVALID_API_KEY   = "fatal_api_key"
    FATAL_SYSTEM_CRASH      = "fatal_system"
    FATAL_CAPTCHA_BLOCK     = "fatal_captcha"
    FATAL_QUOTA_EXCEEDED    = "fatal_quota"

    UNKNOWN = "unknown"


@dataclass
class ClassifiedError:
    original_exception: Exception
    category: ErrorCategory
    tool_name: str
    tool_input: dict
    message: str
    retry_after_sec: Optional[float] = None
    suggested_fallback: Optional[str] = None
    user_message: str = ""
    technical_detail: str = ""

    def is_fatal(self) -> bool:
        return self.category.value.startswith("fatal_")

    def is_transient(self) -> bool:
        return self.category.value.startswith("transient_")

    def is_recoverable(self) -> bool:
        return self.category.value.startswith("recoverable_")


class ErrorClassifier:
    # (pattern, category) — thứ tự quan trọng: specific trước, generic sau
    CLASSIFICATION_RULES = [
        # API key / auth
        (r"invalid.?api.?key|x-api-key|authentication.*failed|unauthorized.*api",
         ErrorCategory.FATAL_INVALID_API_KEY),
        (r"quota.?exceeded|billing|payment.*required|insufficient.*credits",
         ErrorCategory.FATAL_QUOTA_EXCEEDED),

        # Rate limit / overload
        (r"rate.?limit|429|too many requests|request.*limit",
         ErrorCategory.TRANSIENT_RATE_LIMIT),
        (r"overloaded|529|capacity|server.*busy|service.*unavailable",
         ErrorCategory.TRANSIENT_OVERLOAD),

        # Network
        (r"timeout|timed.?out|read timeout|connection.*reset|connection.*refused|eof",
         ErrorCategory.TRANSIENT_NETWORK),

        # Playwright / Browser
        (r"captcha|bot.?detection|access.?denied|blocked.*bot|cf-ray|cloudflare",
         ErrorCategory.FATAL_CAPTCHA_BLOCK),
        (r"session.*expired|login.*required|401.*unauthorized|not.*logged",
         ErrorCategory.RECOVERABLE_AUTH_EXPIRED),
        (r"timeout.*waiting|element.*not.*found|locator.*not.*visible|no.*element|"
         r"strict.*mode.*violation|target.*closed",
         ErrorCategory.RECOVERABLE_ELEMENT_NOT_FOUND),
        (r"net::err|navigation.*failed|page.*crash|frame.*detached|"
         r"navigation.*timeout|failed.*navigate",
         ErrorCategory.RECOVERABLE_NAVIGATION_FAILED),
        (r"content.*changed|stale.*element|element.*detached",
         ErrorCategory.RECOVERABLE_CONTENT_CHANGED),

        # File / Shell
        (r"permission denied|operation not permitted|eperm|eacces",
         ErrorCategory.FATAL_PERMISSION_DENIED),
        (r"no such file|file not found|not exist|enoent",
         ErrorCategory.FATAL_FILE_NOT_EXIST),

        # DB / Lock
        (r"database.*locked|sqlite.*locked|chromadb.*error|collection.*locked",
         ErrorCategory.TRANSIENT_LOCK),
        (r"locked|being used by another|resource.*busy",
         ErrorCategory.TRANSIENT_LOCK),
        (r"collection.*not.*found|no.*collection",
         ErrorCategory.RECOVERABLE_TOOL_WRONG_PARAMS),

        # Rendering
        (r"page.*not.*ready|dom.*not.*loaded|waiting.*render",
         ErrorCategory.TRANSIENT_RENDERING),
    ]

    # tool_name → fallback tool name
    FALLBACK_MAP = {
        "browser_click":           "browser_evaluate",
        "browser_vision_click":    "browser_evaluate",
        "browser_vision_type":     "browser_fill",
        "browser_analyze_page":    "browser_evaluate",
        "browser_navigate":        "run_shell",
        "browser_fill":            "browser_evaluate",
        "screenshot_and_analyze":  "browser_evaluate",
        "recall":                  "recall_broader",
        "run_shell":               "run_applescript",
    }

    USER_MESSAGES = {
        ErrorCategory.TRANSIENT_RATE_LIMIT:
            "API đang bận, Oculo sẽ thử lại sau {retry_after}s...",
        ErrorCategory.TRANSIENT_OVERLOAD:
            "Server đang quá tải, đang thử lại...",
        ErrorCategory.TRANSIENT_NETWORK:
            "Kết nối bị gián đoạn, đang retry...",
        ErrorCategory.TRANSIENT_LOCK:
            "Database đang bận, thử lại ngay...",
        ErrorCategory.TRANSIENT_RENDERING:
            "Trang chưa render xong, đợi thêm...",
        ErrorCategory.RECOVERABLE_ELEMENT_NOT_FOUND:
            "Không tìm thấy element, đang thử cách khác...",
        ErrorCategory.RECOVERABLE_NAVIGATION_FAILED:
            "Điều hướng thất bại, đang thử lại...",
        ErrorCategory.RECOVERABLE_AUTH_EXPIRED:
            "Phiên đăng nhập hết hạn — cần đăng nhập lại.",
        ErrorCategory.RECOVERABLE_CONTENT_CHANGED:
            "Nội dung trang thay đổi, đang thử lại...",
        ErrorCategory.FATAL_CAPTCHA_BLOCK:
            "Trang web phát hiện automation. Cần xử lý thủ công.",
        ErrorCategory.FATAL_PERMISSION_DENIED:
            "Không có quyền thực hiện thao tác này.",
        ErrorCategory.FATAL_INVALID_API_KEY:
            "API key không hợp lệ — kiểm tra lại cấu hình.",
        ErrorCategory.FATAL_QUOTA_EXCEEDED:
            "Đã hết quota API — kiểm tra billing.",
        ErrorCategory.FATAL_FILE_NOT_EXIST:
            "File không tồn tại.",
        ErrorCategory.UNKNOWN:
            "Đã xảy ra lỗi không xác định.",
    }

    @classmethod
    def classify(cls, exc: Exception, tool_name: str,
                 tool_input: dict) -> "ClassifiedError":
        error_str = str(exc)
        category = ErrorCategory.UNKNOWN

        for pattern, cat in cls.CLASSIFICATION_RULES:
            if re.search(pattern, error_str, re.IGNORECASE):
                category = cat
                break

        # Parse retry-after từ error message
        retry_after: Optional[float] = None
        if category == ErrorCategory.TRANSIENT_RATE_LIMIT:
            m = re.search(r"retry.?after[:\s]+(\d+)", error_str, re.IGNORECASE)
            retry_after = float(m.group(1)) if m else 30.0

        fallback = cls.FALLBACK_MAP.get(tool_name)
        _template = cls.USER_MESSAGES.get(
            category, cls.USER_MESSAGES[ErrorCategory.UNKNOWN]
        )
        _ra = int(retry_after or 0)
        try:
            user_msg = _template.format(retry_after=_ra)
        except (KeyError, IndexError):
            user_msg = _template

        return ClassifiedError(
            original_exception=exc,
            category=category,
            tool_name=tool_name,
            tool_input=tool_input,
            message=error_str,
            retry_after_sec=retry_after,
            suggested_fallback=fallback,
            user_message=user_msg,
            technical_detail=f"{type(exc).__name__}: {exc}",
        )
