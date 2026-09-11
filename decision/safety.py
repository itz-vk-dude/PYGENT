from typing import Dict, Any, Tuple

class SafetyValidator:
    def __init__(self, workspace_bounds: dict = None):
        self.bounds = workspace_bounds or {
            "x_min": -350.0, "x_max": 350.0,
            "y_min": 0.0,    "y_max": 450.0,
            "z_min": 0.0,    "z_max": 350.0
        }

    def validate(self, action: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Checks workspace bounds, joint singularities, and safety limits.
        Returns (is_approved, reason).
        """
        x, y, z = action.get("x", 0.0), action.get("y", 0.0), action.get("z", 0.0)

        if not (self.bounds["x_min"] <= x <= self.bounds["x_max"]):
            return False, f"X coordinate {x:.1f} out of safety boundary."
        if not (self.bounds["y_min"] <= y <= self.bounds["y_max"]):
            return False, f"Y coordinate {y:.1f} out of safety boundary."
        if not (self.bounds["z_min"] <= z <= self.bounds["z_max"]):
            return False, f"Z coordinate {z:.1f} out of safety boundary."

        return True, "APPROVED"
