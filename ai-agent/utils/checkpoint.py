"""Lưu checkpoint của conversation để rollback, với TTL và max count."""
import json
import threading
import time
from typing import Optional

_checkpoints: list[dict] = []
_lock = threading.Lock()
MAX_CHECKPOINTS = 20
CHECKPOINT_TTL_SECONDS = 3600  # 1 giờ


def _evict_expired():
    """Xóa checkpoints hết TTL. Phải giữ lock trước khi gọi."""
    cutoff = time.time() - CHECKPOINT_TTL_SECONDS
    global _checkpoints
    _checkpoints = [c for c in _checkpoints if c["ts"] >= cutoff]


def save_checkpoint(messages: list, label: str = "") -> str:
    """Lưu snapshot messages hiện tại."""
    with _lock:
        _evict_expired()
        cp_id = f"cp_{int(time.time() * 1000)}"
        _checkpoints.append({
            "id": cp_id,
            "label": label or f"Checkpoint {len(_checkpoints) + 1}",
            "messages": json.loads(json.dumps(messages)),
            "ts": time.time(),
        })
        if len(_checkpoints) > MAX_CHECKPOINTS:
            _checkpoints.pop(0)
        return cp_id


def list_checkpoints() -> list[dict]:
    with _lock:
        _evict_expired()
        return [{"id": c["id"], "label": c["label"], "ts": c["ts"]} for c in _checkpoints]


def restore_checkpoint(cp_id: str) -> Optional[list]:
    with _lock:
        for cp in _checkpoints:
            if cp["id"] == cp_id:
                return json.loads(json.dumps(cp["messages"]))
    return None


def clear_checkpoints():
    with _lock:
        _checkpoints.clear()
