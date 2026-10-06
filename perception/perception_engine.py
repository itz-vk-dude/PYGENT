import numpy as np
from typing import Dict, Any
from perception.detector import ObjectDetector
from perception.tracker import TrajectoryTracker
from perception.human_understanding import HumanUnderstanding
from perception.scene_understanding import SceneUnderstanding

class PerceptionEngine:
    """
    Public Entry Point for PHYGENT Perception System.
    Combines Detection, Tracking, Human Understanding, and Scene Synthesis.
    """
    def __init__(self):
        self.detector = ObjectDetector()
        self.tracker = TrajectoryTracker()
        self.human_engine = HumanUnderstanding()
        self.scene_engine = SceneUnderstanding()

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Takes raw OpenCV frame and returns unified structured perception state.
        If frame is None (Camera offline), returns offline status structure.
        """
        if frame is None:
            return {
                "status": "CAMERA_OFFLINE",
                "detected": False,
                "person_present": False,
                "x": 0.0, "y": 0.0, "radius": 0.0,
                "vx": 0.0, "vy": 0.0, "speed": 0.0, "direction": 0.0,
                "ax": 0.0, "ay": 0.0,
                "objects": [], "humans": [], "events": ["CAMERA_OFFLINE"],
                "confidence": 0.0, "timestamp": 0.0
            }

        detection = self.detector.detect(frame)
        tracking = self.tracker.update(detection["x"], detection["y"])
        human_info = self.human_engine.analyze(detection, tracking)
        scene = self.scene_engine.synthesize(detection, tracking, human_info)

        return {
            "status": "ONLINE",
            "detected": detection["detected"],
            "person_present": detection["person_present"],
            "x": tracking["x"],
            "y": tracking["y"],
            "radius": detection["radius"],
            "vx": tracking["vx"],
            "vy": tracking["vy"],
            "speed": tracking["speed"],
            "direction": tracking["direction"],
            "ax": tracking["ax"],
            "ay": tracking["ay"],
            "track_id": tracking["track_id"],
            "objects": detection.get("objects", []),
            "scene": scene,
            "human_info": human_info,
            "confidence": detection.get("confidence", 0.0),
            "timestamp": tracking["timestamp"]
        }
