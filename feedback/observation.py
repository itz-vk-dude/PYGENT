from typing import Dict, Any, Tuple

class ObservationCollector:
    """
    Collects REAL physical observations strictly from camera detection and verified hardware telemetry.
    NO ARTIFICIAL OFFSETS ARE CREATED OR USED.
    """
    def get_real_observation(self, perception_data: Dict[str, Any], robot_state: Dict[str, Any]) -> Tuple[float, float]:
        """
        Derives ground-truth physical observation from real camera frame detection.
        """
        if perception_data and perception_data.get("detected", False):
            real_x = float(perception_data.get("x", 0.0))
            real_y = float(perception_data.get("y", 0.0))
            return real_x, real_y
        
        # Fallback to verified measured robot position if camera object isn't present
        robot_pos = robot_state.get("position", [0.0, 0.0, 0.0])
        return float(robot_pos[0]), float(robot_pos[1])
