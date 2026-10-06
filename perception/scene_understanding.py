import time
from typing import Dict, Any, List

class SceneUnderstanding:
    """
    Produces standard structured scene representation JSON.
    """
    def synthesize(self, detection: Dict[str, Any], tracking: Dict[str, Any], human_info: Dict[str, Any]) -> Dict[str, Any]:
        objects_list = detection.get("objects", [])
        humans_list = [obj for obj in objects_list if obj.get("type") == "human"]
        tracked_objects = [obj for obj in objects_list if obj.get("type") != "human"]

        events = []
        if human_info.get("inside_workspace", False):
            events.append("HUMAN_INSIDE_WORKSPACE")
        elif human_info.get("approaching_workspace", False):
            events.append("HUMAN_APPROACHING_WORKSPACE")
        if detection.get("detected", False):
            events.append("OBJECT_DETECTED")

        return {
            "objects": tracked_objects,
            "humans": humans_list,
            "human_summary": human_info,
            "workspace": {
                "center": [320.0, 240.0],
                "status": "OCCUPIED" if human_info.get("inside_workspace") or detection.get("detected") else "CLEAR"
            },
            "events": events,
            "confidence": detection.get("confidence", 0.0),
            "timestamp": tracking.get("timestamp", time.time())
        }
