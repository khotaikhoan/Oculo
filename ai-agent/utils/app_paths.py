"""
Đường dẫn tài nguyên và dữ liệu — an toàn cho cả mode dev lẫn PyInstaller .app.

Bundle `.app` của macOS là read-only. Mọi ChromaDB / SQLite / session / log phải
ghi vào `~/Library/Application Support/Oculo`; resource chỉ đọc (static/, icon)
nằm trong `sys._MEIPASS` khi frozen, còn ở dev mode là thư mục repo.
"""
import os
import sys
from pathlib import Path


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def app_support_dir() -> Path:
    """Thư mục dữ liệu ghi được, ổn định giữa các bản cài đặt."""
    override = os.getenv("OCULO_DATA_DIR")
    if override:
        base = Path(override).expanduser()
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support" / "Oculo"
    elif sys.platform == "win32":
        root = os.getenv("APPDATA") or str(Path.home())
        base = Path(root) / "Oculo"
    else:
        xdg = os.getenv("XDG_DATA_HOME")
        base = Path(xdg).expanduser() if xdg else Path.home() / ".local" / "share"
        base = base / "Oculo"
    base.mkdir(parents=True, exist_ok=True)
    return base


_REPO_ROOT = Path(__file__).resolve().parent.parent


def data_dir(subdir: str = "") -> Path:
    """Nơi lưu dữ liệu ghi được. Dev: gốc repo. Frozen: Application Support."""
    base = app_support_dir() if is_frozen() else _REPO_ROOT
    p = base / subdir if subdir else base
    p.mkdir(parents=True, exist_ok=True)
    return p


def resource_dir() -> Path:
    """Thư mục chứa resource chỉ đọc (static/, icon) — trong bundle hay repo."""
    if is_frozen():
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            return Path(meipass)
    return _REPO_ROOT


def dotenv_path() -> str | None:
    """
    Tìm `.env`:
      1. `OCULO_ENV_FILE` nếu được set.
      2. `~/Library/Application Support/Oculo/.env` (tạo mới sau cài đặt).
      3. `<resource_dir>/.env.example` bundled kèm .app (đọc được).
      4. `<repo_root>/.env` khi chạy dev.
    Trả về None nếu không tìm thấy — `load_dotenv(None)` sẽ an toàn, chỉ dùng env hệ thống.
    """
    override = os.getenv("OCULO_ENV_FILE")
    if override and Path(override).expanduser().is_file():
        return str(Path(override).expanduser())

    candidates = [
        app_support_dir() / ".env",
        resource_dir() / ".env.example",
        _REPO_ROOT / ".env",
    ]
    for c in candidates:
        if c.is_file():
            return str(c)
    return None
