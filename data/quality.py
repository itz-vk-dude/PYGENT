import time
from typing import Dict, Any

class DataQualityChecker:
    """
    Data Quality Audit Module.
    Validates physical data consistency, range bounds, maximum velocity sanity, and latency.
    CRITICAL RULE: BAD DATA -> DO NOT AUTOMATICALLY ACT.
    """
    def __init__(self, max_speed_px_per_sec: float = 2000.0, max_stale_sec: float = 2.0):
        self.max_speed = max_speed_px_per_sec
        self.max_stale_sec = max_stale_sec

    def check_quality(self, perception_data: Dict[str, Any]) -> Dict[str, Any]:
        if not perception_data:
            return {"status": "BAD_DATA", "reason": "Empty perception state", "allow_action": False}

        if not perception_data.get("detected", False) and not perception_data.get("person_present", False):
            return {"status": "NO_DETECTION", "reason": "No active objects/persons detected", "allow_action": False}

        # Check timestamp staleness
        ts = perception_data.get("timestamp", 0.0)
        if ts > 0 and (time.time() - ts) > self.max_stale_sec:
            return {"status": "STALE_DATA", "reason": f"Data latency higher than {self.max_stale_sec}s", "allow_action": False}

        # Check speed bounds
        speed = perception_data.get("speed", 0.0)
        if speed > self.max_speed:
            return {"status": "IMPOSSIBLE_VELOCITY", "reason": f"Speed {speed:.1f} px/s exceeds maximum {self.max_speed} px/s", "allow_action": False}

        # Check coordinate range sanity
        x = perception_data.get("x", 0.0)
        y = perception_data.get("y", 0.0)
        if x < -1000.0 or x > 2000.0 or y < -1000.0 or y > 2000.0:
            return {"status": "OUT_OF_RANGE", "reason": f"Coordinates ({x}, {y}) out of plausible visual range", "allow_action": False}

        return {"status": "NORMAL", "reason": "Data passed all quality checks", "allow_action": True}
