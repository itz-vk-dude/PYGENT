from typing import Tuple

class CoordinateCalibrator:
    """
    Affine transformation from Camera Pixels (px) to Robot Spatial World Space (mm).
    """
    def __init__(self, scale_x: float = 0.5, scale_y: float = 0.5, offset_x: float = 100.0, offset_y: float = 50.0, default_z: float = 150.0):
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.cx = 320.0
        self.cy = 240.0
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.default_z = default_z

    def pixel_to_robot(self, px_x: float, px_y: float, target_z: float = None) -> Tuple[float, float, float]:
        robot_x = (px_x - self.cx) * self.scale_x + self.offset_x
        robot_y = (px_y - self.cy) * self.scale_y + self.offset_y
        robot_z = target_z if target_z is not None else self.default_z

        return float(robot_x), float(robot_y), float(robot_z)

    def robot_to_pixel(self, robot_x: float, robot_y: float) -> Tuple[float, float]:
        px_x = ((robot_x - self.offset_x) / self.scale_x) + self.cx
        px_y = ((robot_y - self.offset_y) / self.scale_y) + self.cy
        return float(px_x), float(px_y)
