from enum import Enum


class JobStatuses(str, Enum):
    COMPLETED = "completed"
    RUNNING = "running"
    FAILED = "failed"
    PENDING = "pending"
    PAUSED = "paused"
