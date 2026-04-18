"""
Task Progress Store — SQLite-backed checkpoint system.
Cho phép resume task dài khi fail ở bước giữa chừng.
"""
import json
import time
import sqlite3
import uuid
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Any

DB_PATH = Path(__file__).parent.parent / "data" / "task_progress.db"


@dataclass
class TaskStep:
    step_index: int
    tool_name: str
    tool_input: dict
    result: Any
    status: str           # pending | success | failed | skipped | success_via_fallback
    attempts: int
    error_category: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class TaskProgress:
    task_id: str
    conversation_id: str
    original_query: str
    total_steps_estimated: int
    steps: List[TaskStep]
    status: str           # running | paused | completed | failed
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    @property
    def completed_steps(self) -> int:
        return sum(1 for s in self.steps
                   if s.status in ("success", "success_via_fallback", "skipped"))

    @property
    def last_successful_step(self) -> Optional[TaskStep]:
        done = [s for s in self.steps
                if s.status in ("success", "success_via_fallback", "skipped")]
        return done[-1] if done else None

    def to_summary(self) -> str:
        return (
            f"Task {self.task_id[:8]}: {self.completed_steps}/{len(self.steps)} bước "
            f"({self.status}) — '{self.original_query[:60]}'"
        )


class ProgressStore:
    """SQLite-backed store — persist qua server restart, không cần Redis."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path, timeout=10.0) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS task_progress (
                    task_id        TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    data           TEXT NOT NULL,
                    status         TEXT NOT NULL,
                    created_at     REAL NOT NULL,
                    updated_at     REAL NOT NULL
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_conv "
                "ON task_progress(conversation_id, updated_at)"
            )

    def save(self, progress: TaskProgress):
        progress.updated_at = time.time()
        data = asdict(progress)
        with sqlite3.connect(self.db_path, timeout=10.0) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO task_progress VALUES (?,?,?,?,?,?)",
                (
                    progress.task_id,
                    progress.conversation_id,
                    json.dumps(data),
                    progress.status,
                    progress.created_at,
                    progress.updated_at,
                ),
            )

    def load(self, task_id: str) -> Optional[TaskProgress]:
        with sqlite3.connect(self.db_path, timeout=10.0) as conn:
            row = conn.execute(
                "SELECT data FROM task_progress WHERE task_id = ?", (task_id,)
            ).fetchone()
        if not row:
            return None
        return self._deserialize(row[0])

    def get_resumable(self, conversation_id: str,
                      max_age_sec: int = 3600) -> List[TaskProgress]:
        """Tasks có thể resume trong conversation này (1 giờ gần nhất)."""
        cutoff = time.time() - max_age_sec
        with sqlite3.connect(self.db_path, timeout=10.0) as conn:
            rows = conn.execute(
                """SELECT data FROM task_progress
                   WHERE conversation_id = ?
                     AND status IN ('paused', 'running', 'failed')
                     AND updated_at > ?
                   ORDER BY updated_at DESC LIMIT 5""",
                (conversation_id, cutoff),
            ).fetchall()
        return [self._deserialize(r[0]) for r in rows]

    def mark_completed(self, task_id: str):
        with sqlite3.connect(self.db_path, timeout=10.0) as conn:
            conn.execute(
                "UPDATE task_progress SET status='completed', updated_at=? WHERE task_id=?",
                (time.time(), task_id),
            )

    def _deserialize(self, json_str: str) -> TaskProgress:
        data = json.loads(json_str)
        data["steps"] = [TaskStep(**s) for s in data["steps"]]
        return TaskProgress(**data)


# Singleton
progress_store = ProgressStore()


def create_task(conversation_id: str, query: str,
                estimated_steps: int = 10) -> TaskProgress:
    """Tạo task mới và lưu vào store."""
    task = TaskProgress(
        task_id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        original_query=query,
        total_steps_estimated=estimated_steps,
        steps=[],
        status="running",
    )
    progress_store.save(task)
    return task


def record_step(task: TaskProgress, tool_name: str, tool_input: dict,
                result: Any, status: str, attempts: int,
                error_category: str = "") -> TaskStep:
    """Ghi một bước vào task và persist."""
    step = TaskStep(
        step_index=len(task.steps),
        tool_name=tool_name,
        tool_input=tool_input,
        result=str(result)[:500] if result else None,
        status=status,
        attempts=attempts,
        error_category=error_category,
    )
    task.steps.append(step)
    progress_store.save(task)
    return step
