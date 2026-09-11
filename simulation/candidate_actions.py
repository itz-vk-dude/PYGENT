from calibration.camera_robot_mapping import CoordinateCalibrator
from typing import List, Dict, Any

class CandidateActionGenerator:
    def __init__(self):
        self.calibrator = CoordinateCalibrator()

    def generate_actions(self, hybrid_pred: tuple, current_pos: tuple) -> List[Dict[str, Any]]:
        """
        Generates candidate spatial actions (A, B, C) in robot mm coordinates based on hybrid trajectory prediction.
        """
        pred_x, pred_y = hybrid_pred
        
        # Action A: Direct predicted interception point
        rx_a, ry_a, rz_a = self.calibrator.pixel_to_robot(pred_x, pred_y, target_z=150.0)

        # Action B: Early lead point (offset along approach vector)
        rx_b, ry_b, rz_b = self.calibrator.pixel_to_robot(pred_x - 20.0, pred_y - 10.0, target_z=150.0)

        # Action C: Defensive safe point (further back)
        rx_c, ry_c, rz_c = self.calibrator.pixel_to_robot(pred_x + 20.0, pred_y + 10.0, target_z=150.0)

        return [
            {"id": "A", "name": "Direct Intercept", "x": rx_a, "y": ry_a, "z": rz_a, "target_px": (pred_x, pred_y)},
            {"id": "B", "name": "Early Lead Intercept", "x": rx_b, "y": ry_b, "z": rz_b, "target_px": (pred_x - 20.0, pred_y - 10.0)},
            {"id": "C", "name": "Defensive Intercept", "x": rx_c, "y": ry_c, "z": rz_c, "target_px": (pred_x + 20.0, pred_y + 10.0)}
        ]
