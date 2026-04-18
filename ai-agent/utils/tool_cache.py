"""
Tool Cache — cache kết quả run_shell cho các lệnh read-only với TTL 60s.
Requirements: 10.1 - 10.6
"""
import threading
import time
import re
from dataclasses import dataclass, field
from typing import Optional

# Các lệnh read-only được phép cache
READ_ONLY_COMMANDS = {"ps", "df", "uname", "date", "whoami", "hostname", "uptime", "sw_vers", "arch", "id"}

# Pattern phát hiện lệnh không an toàn để cache
UNSAFE_PATTERN = re.compile(r'[|><$`]')


@dataclass
class CacheEntry:
    result: str
    created_at: float = field(default_factory=time.time)
    ttl: int = 60

    def is_valid(self) -> bool:
        return (time.time() - self.created_at) < self.ttl


_cache: dict[str, CacheEntry] = {}
_cache_lock = threading.Lock()


def is_cacheable(cmd: str) -> bool:
    """Kiểm tra lệnh có thể cache không."""
    if not cmd or not cmd.strip():
        return False
    if UNSAFE_PATTERN.search(cmd):
        return False
    base_cmd = cmd.strip().split()[0]
    return base_cmd in READ_ONLY_COMMANDS


def get_cached(cmd: str) -> Optional[str]:
    """Lấy kết quả từ cache nếu còn hợp lệ."""
    with _cache_lock:
        entry = _cache.get(cmd)
        if entry is None:
            return None
        if entry.is_valid():
            return entry.result
        del _cache[cmd]
        return None


def set_cache(cmd: str, result: str) -> None:
    """Lưu kết quả vào cache."""
    with _cache_lock:
        _cache[cmd] = CacheEntry(result=result)


def clear_cache() -> None:
    """Xóa toàn bộ cache (dùng cho testing)."""
    with _cache_lock:
        _cache.clear()


def cache_size() -> int:
    with _cache_lock:
        return len(_cache)
