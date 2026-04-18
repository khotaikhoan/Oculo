"""Xoay vòng nhiều API keys để tránh rate limit."""
import os
import time
from dotenv import load_dotenv

load_dotenv()


class ApiKeyManager:
    def __init__(self):
        prefix = "ANTHROPIC_API_KEY"
        self.keys = []
        for i in range(1, 6):
            suffix = "" if i == 1 else f"_{i}"
            key = os.getenv(f"{prefix}{suffix}")
            if key:
                self.keys.append({"key": key, "last_used": 0, "errors": 0})
        if not self.keys:
            raise ValueError(
                f"No API keys found (expected {prefix} or {prefix}_2 …). "
                "Đặt ANTHROPIC_API_KEY trong .env (Anthropic hoặc endpoint tương thích Messages API)."
            )
        self._current = 0

    def get_key(self) -> str:
        """Lấy key ít lỗi nhất và ít dùng nhất."""
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


key_manager = ApiKeyManager()
