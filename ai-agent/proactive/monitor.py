"""
Proactive agent - background monitors for files, calendar, and system events.
Notifies user and can auto-trigger agent tasks.
"""
import os
import json
import time
import threading
import subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Global state
_monitors: dict = {}
_observer: Observer = None
_callbacks: list = []  # list of callables(event_type, data)
_lock = threading.Lock()


def add_callback(fn):
    """Register a callback for proactive events."""
    _callbacks.append(fn)


def _notify(event_type: str, data: dict):
    """Fire all registered callbacks."""
    for cb in _callbacks:
        try:
            cb(event_type, data)
        except Exception:
            pass


def _send_macos_notification(title: str, message: str):
    t_esc = str(title).replace("\\", "\\\\").replace('"', '\\"')
    m_esc = str(message).replace("\\", "\\\\").replace('"', '\\"')
    script = f'display notification "{m_esc}" with title "{t_esc}"'
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        return
    if result.returncode != 0:
        pass


# ── File Monitor ──
class _FileHandler(FileSystemEventHandler):
    def __init__(self, watch_id: str, patterns: list[str]):
        self.watch_id = watch_id
        self.patterns = patterns
        self._last_event = {}

    def _matches(self, path: str) -> bool:
        if not self.patterns:
            return True
        return any(path.endswith(p.lstrip("*")) for p in self.patterns)

    def _debounce(self, path: str) -> bool:
        now = time.time()
        last = self._last_event.get(path, 0)
        if now - last < 2:
            return False
        self._last_event[path] = now
        return True

    def on_created(self, event):
        if not event.is_directory and self._matches(event.src_path) and self._debounce(event.src_path):
            data = {"watch_id": self.watch_id, "path": event.src_path, "event": "created"}
            _notify("file_created", data)
            _send_macos_notification("AI Agent - File Monitor", f"New file: {os.path.basename(event.src_path)}")

    def on_modified(self, event):
        if not event.is_directory and self._matches(event.src_path) and self._debounce(event.src_path):
            data = {"watch_id": self.watch_id, "path": event.src_path, "event": "modified"}
            _notify("file_modified", data)

    def on_deleted(self, event):
        if not event.is_directory and self._matches(event.src_path) and self._debounce(event.src_path):
            data = {"watch_id": self.watch_id, "path": event.src_path, "event": "deleted"}
            _notify("file_deleted", data)
            _send_macos_notification("AI Agent - File Monitor", f"File deleted: {os.path.basename(event.src_path)}")


def start_file_monitor(watch_id: str, path: str, patterns: list[str] = None) -> dict:
    """Start monitoring a directory for file changes."""
    global _observer
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return {"ok": False, "error": f"Path not found: {path}"}

    if _observer is None:
        _observer = Observer()
        _observer.start()

    handler = _FileHandler(watch_id, patterns or [])
    watch = _observer.schedule(handler, path, recursive=True)

    with _lock:
        _monitors[watch_id] = {
            "type": "file",
            "path": path,
            "patterns": patterns,
            "watch": watch,
            "created": datetime.now().isoformat()
        }
    return {"ok": True, "watch_id": watch_id, "path": path}


# ── Calendar Monitor ──
def _check_calendar():
    """Check upcoming calendar events via AppleScript."""
    script = '''
    tell application "Calendar"
        set now to current date
        set soon to now + (30 * minutes)
        set upcoming to {}
        repeat with cal in calendars
            repeat with ev in (events of cal whose start date >= now and start date <= soon)
                set end of upcoming to (summary of ev) & " at " & (time string of (start date of ev))
            end repeat
        end repeat
        return upcoming
    end tell
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
    return result.stdout.strip()


def start_calendar_monitor(watch_id: str, interval_minutes: int = 5) -> dict:
    """Poll calendar every N minutes for upcoming events."""
    def _poll():
        while watch_id in _monitors:
            try:
                events = _check_calendar()
                if events and events != "{}":
                    data = {"watch_id": watch_id, "events": events}
                    _notify("calendar_event", data)
                    _send_macos_notification("AI Agent - Calendar", f"Upcoming: {events[:80]}")
            except Exception:
                pass
            time.sleep(interval_minutes * 60)

    t = threading.Thread(target=_poll, daemon=True)
    t.start()
    with _lock:
        _monitors[watch_id] = {
            "type": "calendar",
            "interval_minutes": interval_minutes,
            "thread": t,
            "created": datetime.now().isoformat()
        }
    return {"ok": True, "watch_id": watch_id}


# ── System Monitor ──
def start_system_monitor(watch_id: str, cpu_threshold: float = 90.0,
                          mem_threshold: float = 90.0, interval: int = 30) -> dict:
    """Monitor CPU/RAM and alert when thresholds exceeded."""
    def _poll():
        while watch_id in _monitors:
            try:
                try:
                    import psutil
                    cpu = psutil.cpu_percent(interval=1)
                    mem_pct = psutil.virtual_memory().percent
                except ImportError:
                    # Fallback nếu psutil chưa cài
                    cpu_out = subprocess.run(
                        ["bash", "-c", "top -l 1 -s 0 | grep 'CPU usage' | awk '{print $3}' | tr -d '%'"],
                        capture_output=True, text=True, timeout=10,
                    ).stdout.strip()
                    cpu = float(cpu_out or "0")

                    mem_out = subprocess.run(
                        ["bash", "-c", "vm_stat | grep 'Pages active' | awk '{print $3}' | tr -d '.'"],
                        capture_output=True, text=True, timeout=5,
                    ).stdout.strip()
                    mem_pages = int(mem_out or "0")
                    mem_gb = (mem_pages * 16384) / (1024 ** 3)
                    total_mem = float(subprocess.run(
                        ["bash", "-c", "sysctl hw.memsize | awk '{print $2}'"],
                        capture_output=True, text=True, timeout=5,
                    ).stdout.strip() or "1") / (1024 ** 3)
                    mem_pct = (mem_gb / total_mem * 100) if total_mem > 0 else 0

                alerts = []
                if cpu > cpu_threshold:
                    alerts.append(f"CPU: {cpu:.1f}%")
                if mem_pct > mem_threshold:
                    alerts.append(f"RAM: {mem_pct:.1f}%")

                if alerts:
                    msg = "High usage: " + ", ".join(alerts)
                    _notify("system_alert", {"watch_id": watch_id, "message": msg, "cpu": cpu, "mem_pct": mem_pct})
                    _send_macos_notification("AI Agent - System Alert", msg)
            except Exception:
                pass
            time.sleep(interval)

    t = threading.Thread(target=_poll, daemon=True)
    t.start()
    with _lock:
        _monitors[watch_id] = {
            "type": "system",
            "cpu_threshold": cpu_threshold,
            "mem_threshold": mem_threshold,
            "interval": interval,
            "thread": t,
            "created": datetime.now().isoformat()
        }
    return {"ok": True, "watch_id": watch_id}


def stop_monitor(watch_id: str) -> dict:
    """Stop a monitor."""
    with _lock:
        m = _monitors.pop(watch_id, None)
    if not m:
        return {"ok": False, "error": "Monitor not found"}
    if m["type"] == "file" and _observer:
        try:
            _observer.unschedule(m["watch"])
        except Exception:
            pass
    return {"ok": True}


def list_monitors() -> dict:
    """List all active monitors."""
    with _lock:
        return {k: {kk: vv for kk, vv in v.items() if kk not in ("watch", "thread")}
                for k, v in _monitors.items()}


def stop_all():
    """Stop all monitors."""
    global _observer
    with _lock:
        _monitors.clear()
    if _observer:
        _observer.stop()
        _observer = None
