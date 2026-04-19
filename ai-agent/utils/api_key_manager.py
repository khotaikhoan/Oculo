"""Xoay vòng nhiều API keys để tránh rate limit."""
import os
import time
from dotenv import load_dotenv

load_dotenv()


class _NoKeysError(RuntimeError):
    def __init__(self):
        super().__init__(
            "No API keys found. Đặt một trong: ANTHROPIC_API_KEY (Anthropic hoặc proxy Messages), "
            "CHIASEGPU_API_KEY (chiasegpu), hoặc GEMINI_API_KEY + GEMINI_BASE_URL (chat qua /v1). "
            "Nếu proxy dùng chung token cho cả Messages và /v1: thêm ANTHROPIC_BASE_URL để SDK Anthropic dùng cùng GEMINI_API_KEY."
        )


class ApiKeyManager:
    def __init__(self):
        self.keys = []
        self._current = 0
        self.reload()

    def reload(self):
        """Đọc lại keys từ môi trường — gọi khi .env được cập nhật sau khi app chạy."""
        prefix = "ANTHROPIC_API_KEY"
        self.keys = []
        for i in range(1, 6):
            suffix = "" if i == 1 else f"_{i}"
            key = os.getenv(f"{prefix}{suffix}")
            if key:
                self.keys.append({"key": key, "last_used": 0, "errors": 0})

        def _add_unique(raw: str | None):
            k = (raw or "").strip()
            if not k or any(x["key"] == k for x in self.keys):
                return
            self.keys.append({"key": k, "last_used": 0, "errors": 0})

        # Chiasegpu / proxy Messages (một key, không bắt buộc đặt tên ANTHROPIC_*)
        _add_unique(os.getenv("CHIASEGPU_API_KEY"))
        _add_unique(os.getenv("ANTHROPIC_DELEGATE_API_KEY"))

        # Cùng token OpenAI-compat + Messages trên một proxy (vd. chiasegpu): cần ANTHROPIC_BASE_URL
        if (os.getenv("ANTHROPIC_BASE_URL") or "").strip():
            _add_unique(os.getenv("GEMINI_API_KEY"))
            _add_unique(os.getenv("OPENAI_COMPAT_API_KEY"))

    def get_key(self) -> str:
        """Lấy key ít lỗi nhất và ít dùng nhất. Raise nếu chưa có key."""
        if not self.keys:
            # Thử nạp lại phòng trường hợp .env vừa được tạo sau khi app khởi động.
            self.reload()
            if not self.keys:
                raise _NoKeysError()
        if len(self.keys) == 1:
            return self.keys[0]["key"]
        best = min(self.keys, key=lambda k: (k["errors"], k["last_used"]))
        best["last_used"] = time.time()
        return best["key"]

    def report_error(self, key: str, is_rate_limit: bool = False):
        """Báo cáo lỗi cho key."""
        for k in self.keys:
            if k["key"] == key:
                k["errors"] += 2 if is_rate_limit else 1
                break

    def report_success(self, key: str):
        """Reset error count khi thành công."""
        for k in self.keys:
            if k["key"] == key:
                k["errors"] = max(0, k["errors"] - 1)
                break

    @property
    def count(self) -> int:
        return len(self.keys)


# Không raise ở import time — app phải khởi động được cả khi người dùng
# chưa có .env (ví dụ ngay sau khi cài từ .dmg, chưa điền API key).
key_manager = ApiKeyManager()
