from perception.object_detection import ObjectDetector
from perception.tracking import TrajectoryTracker
from typing import Dict, Any
import numpy as np

class PerceptionEngine:
    def __init__(self):
        self.detector = ObjectDetector()
        self.tracker = TrajectoryTracker()

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Takes a raw OpenCV frame, performs color segmentation detection & tracking,
        and returns structured perception state.
        """
        detection = self.detector.detect(frame)
        if detection["detected"] or detection["person_present"]:
            tracking_info = self.tracker.update(detection["x"], detection["y"])
            return {
                "detected": detection["detected"],
                "person_present": detection["person_present"],
                "x": tracking_info["x"],
                "y": tracking_info["y"],
                "radius": detection["radius"],
                "objects": detection.get("objects", []),
                "vx": tracking_info["vx"],
                "vy": tracking_info["vy"],
                "speed": tracking_info["speed"],
                "direction": tracking_info["direction"],
                "ax": tracking_info["ax"],
                "ay": tracking_info["ay"],
                "timestamp": tracking_info["timestamp"]
            }
        else:
            return {
                "detected": False,
                "person_present": False,
                "x": 0.0,
                "y": 0.0,
                "radius": 0.0,
                "objects": [],
                "vx": 0.0,
                "vy": 0.0,
                "speed": 0.0,
                "direction": 0.0,
                "ax": 0.0,
                "ay": 0.0,
                "timestamp": 0.0
            }

