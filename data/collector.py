from typing import Dict, Any, List
import time

class DataCollector:
    """
    Data Collection Buffer for batch processing and model training datasets.
    """
    def __init__(self, max_buffer_size: int = 1000):
        self.max_buffer_size = max_buffer_size
        self.buffer: List[Dict[str, Any]] = []

    def collect(self, state: Dict[str, Any]):
        entry = dict(state)
        entry["collected_at"] = time.time()
        self.buffer.append(entry)
        if len(self.buffer) > self.max_buffer_size:
            self.buffer.pop(0)

    def get_recent(self, n: int = 50) -> List[Dict[str, Any]]:
        return self.buffer[-n:]

    def clear(self):
        self.buffer.clear()
