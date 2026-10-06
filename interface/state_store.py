import threading
from typing import Dict, Any

class StateStore:
    """
    Thread-safe State Store interfacing between PHYGENT Agent Core and Flask HTTP/SSE Endpoints.
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.data: Dict[str, Any] = {}

    def update(self, new_data: Dict[str, Any]):
        with self.lock:
            self.data = dict(new_data)

    def get(self) -> Dict[str, Any]:
        with self.lock:
            return dict(self.data)
