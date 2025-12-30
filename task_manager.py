"""
Task Manager for BYRD - Structured Task Execution Framework
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Callable, Any


class TaskStatus(Enum):
    """Possible states for a task."""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Priority levels for task scheduling."""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4


@dataclass
class Task:
    """Represents a single autonomous task in the system."""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Unnamed Task"
    description: str = ""
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0
    depends_on: List[str] = field(default_factory=list)
    action: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_by: str = "system"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        data['priority'] = TaskPriority(data['priority'])
        data['status'] = TaskStatus(data['status'])
        return cls(**data)
    
    def is_ready(self, completed_tasks: set) -> bool:
        return all(dep_id in completed_tasks for dep_id in self.depends_on)


class TaskManager:
    """Manages task lifecycle, scheduling, and execution coordination."""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
    
    def add_task(self, task: Task) -> str:
        self.tasks[task.task_id] = task
        self._resolve_dependencies()
        return task.task_id
    
    def create_task(self, name: str, description: str = "", priority: TaskPriority = TaskPriority.NORMAL, action: Optional[str] = None, parameters: Optional[Dict[str, Any]] = None, depends_on: Optional[List[str]] = None, tags: Optional[List[str]] = None, created_by: str = "system") -> Task:
        task = Task(name=name, description=description, priority=priority, action=action, parameters=parameters or {}, depends_on=depends_on or [], tags=tags or [], created_by=created_by)
        self.add_task(task)
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        return [t for t in self.tasks.values() if t.status == status]
    
    def get_ready_tasks(self) -> List[Task]:
        completed_ids = {t_id for t_id, t in self.tasks.items() if t.status == TaskStatus.COMPLETED}
        ready = []
        for task in self.tasks.values():
            if task.status in [TaskStatus.READY, TaskStatus.PENDING]:
                if task.is_ready(completed_ids):
                    ready.append(task)
        ready.sort(key=lambda t: t.priority.value)
        return ready
    
    def start_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if task and task.status == TaskStatus.READY:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now().isoformat()
            return True
        return False
    
    def complete_task(self, task_id: str, result: Any = None) -> bool:
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            task.progress = 1.0
            if result is not None:
                task.result = result
            self._resolve_dependencies()
            return True
        return False
    
    def fail_task(self, task_id: str, error: str) -> bool:
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now().isoformat()
            task.error = error
            return True
        return False
    
    def _resolve_dependencies(self):
        completed_ids = {t_id for t_id, t in self.tasks.items() if t.status == TaskStatus.COMPLETED}
        for task in self.tasks.values():
            if task.status in [TaskStatus.PENDING, TaskStatus.BLOCKED]:
                if task.is_ready(completed_ids):
                    task.status = TaskStatus.READY
                elif task.depends_on:
                    task.status = TaskStatus.BLOCKED
    
    def get_statistics(self) -> Dict[str, Any]:
        stats = {'total': len(self.tasks), 'by_status': {}, 'by_priority': {}, 'progress_avg': 0.0}
        for task in self.tasks.values():
            status_name = task.status.value
            stats['by_status'][status_name] = stats['by_status'].get(status_name, 0) + 1
            priority_name = task.priority.name
            stats['by_priority'][priority_name] = stats['by_priority'].get(priority_name, 0) + 1
            stats['progress_avg'] += task.progress
        if self.tasks:
            stats['progress_avg'] /= len(self.tasks)
        return stats


class TaskExecutor:
    """Executes tasks using registered handlers."""
    
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.handlers: Dict[str, Callable] = {}
        self.default_handler: Optional[Callable] = None
    
    def register_handler(self, action: str, handler: Callable):
        self.handlers[action] = handler
    
    def register_default_handler(self, handler: Callable):
        self.default_handler = handler
    
    def execute_task(self, task: Task) -> Any:
        self.task_manager.start_task(task.task_id)
        try:
            handler = None
            if task.action and task.action in self.handlers:
                handler = self.handlers[task.action]
            elif self.default_handler:
                handler = self.default_handler
            if handler:
                result = handler(task)
                self.task_manager.complete_task(task.task_id, result)
                return result
            else:
                raise ValueError(f"No handler for action: {task.action}")
        except Exception as e:
            self.task_manager.fail_task(task.task_id, str(e))
            raise
    
    def execute_ready_tasks(self, limit: Optional[int] = None) -> int:
        ready_tasks = self.task_manager.get_ready_tasks()
        if limit:
            ready_tasks = ready_tasks[:limit]
        executed = 0
        for task in ready_tasks:
            try:
                self.execute_task(task)
                executed += 1
            except Exception:
                pass
        return executed


if __name__ == "__main__":
    manager = TaskManager()
    task1 = manager.create_task(name="Test task", description="A test task", priority=TaskPriority.HIGH)
    print(f"Created task: {task1.task_id}")
    stats = manager.get_statistics()
    print(f"Stats: {stats}")
