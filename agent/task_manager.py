from typing import Dict, Any

class TaskManager:
    """
    Task State Tracking Module.
    Tracks active task, origin, priority, status, goal, progress, and result.
    """
    def __init__(self):
        self.current_task = "PERCEPTION_TRACKING"
        self.priority = 1
        self.status = "WAITING"
        self.progress = 0.0

    def update_task(self, name: str, status: str = "IN_PROGRESS", progress: float = 0.0):
        self.current_task = name
        self.status = status
        self.progress = progress

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.current_task,
            "priority": self.priority,
            "status": self.status,
            "progress": round(self.progress, 2)
        }
