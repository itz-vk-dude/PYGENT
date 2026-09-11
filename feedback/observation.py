from typing import Dict, Any

class ObservationCollector:
    def collect_actual(self, perception_data: Dict[str, Any], esp32_feedback: Dict[str, Any] = None) -> Dict[str, Any]:
        return {
            "actual_x": perception_data.get("x", 0.0),
            "actual_y": perception_data.get("y", 0.0),
            "status": "COMPLETED",
            "timestamp": perception_data.get("timestamp", 0.0)
        }
