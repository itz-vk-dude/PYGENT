import math
import time
from typing import Dict, List, Any

class TrajectoryTracker:
    """
    Trajectory Tracker.
    Calculates velocity (vx, vy), speed, direction, acceleration (ax, ay), and assigns track_id.
    """
    def __init__(self, history_len: int = 10):
        self.history_len = history_len
        self.history: List[Dict[str, float]] = []
        self.track_id = 1

    def update(self, x: float, y: float, timestamp: float = None) -> Dict[str, Any]:
        if timestamp is None:
            timestamp = time.time()

        point = {"x": x, "y": y, "timestamp": timestamp}
        self.history.append(point)
        if len(self.history) > self.history_len:
            self.history.pop(0)

        vx, vy = 0.0, 0.0
        ax, ay = 0.0, 0.0
        speed = 0.0
        direction = 0.0

        if len(self.history) >= 2:
            dt = self.history[-1]["timestamp"] - self.history[-2]["timestamp"]
            if dt > 1e-5:
                vx = (self.history[-1]["x"] - self.history[-2]["x"]) / dt
                vy = (self.history[-1]["y"] - self.history[-2]["y"]) / dt
                speed = math.sqrt(vx**2 + vy**2)
                direction = math.degrees(math.atan2(vy, vx))

        if len(self.history) >= 3:
            dt1 = self.history[-2]["timestamp"] - self.history[-3]["timestamp"]
            dt2 = self.history[-1]["timestamp"] - self.history[-2]["timestamp"]
            if dt1 > 1e-5 and dt2 > 1e-5:
                vx_prev = (self.history[-2]["x"] - self.history[-3]["x"]) / dt1
                vy_prev = (self.history[-2]["y"] - self.history[-3]["y"]) / dt1
                dt_avg = 0.5 * (dt1 + dt2)
                ax = (vx - vx_prev) / dt_avg
                ay = (vy - vy_prev) / dt_avg

        return {
            "track_id": self.track_id,
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "speed": speed,
            "direction": direction,
            "ax": ax,
            "ay": ay,
            "timestamp": timestamp
        }

    def reset(self):
        self.history.clear()
        self.track_id += 1
