import numpy as np
from typing import Tuple

class CoordinateCalibrator:
    def __init__(self):
        """
        Affine transformation from Camera Pixels (px) to Robot World Space (mm).
        Robot_X = scale_x * (px_x - cx) + offset_x
        Robot_Y = scale_y * (px_y - cy) + offset_y
        Robot_Z = target_z (default 150 mm)
        """
        self.scale_x = 0.5    # mm per pixel
        self.scale_y = 0.5    # mm per pixel
        self.cx = 320.0       # camera center pixel x
        self.cy = 240.0       # camera center pixel y
        self.offset_x = 100.0 # robot base origin offset X (mm)
        self.offset_y = 50.0  # robot base origin offset Y (mm)
        self.default_z = 150.0# robot default intercept height Z (mm)

    def set_calibration(self, scale_x: float, scale_y: float, offset_x: float, offset_y: float, default_z: float = 150.0):
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.default_z = default_z

    def pixel_to_robot(self, px_x: float, px_y: float, target_z: float = None) -> Tuple[float, float, float]:
        """
        Converts camera frame pixel coordinates (px_x, px_y) to robot spatial coordinates (X, Y, Z) in mm.
        """
        robot_x = (px_x - self.cx) * self.scale_x + self.offset_x
        robot_y = (px_y - self.cy) * self.scale_y + self.offset_y
        robot_z = target_z if target_z is not None else self.default_z

        return float(robot_x), float(robot_y), float(robot_z)

    def robot_to_pixel(self, robot_x: float, robot_y: float) -> Tuple[float, float]:
        """
        Converts robot coordinates (X, Y) back to camera pixel coordinates (px_x, px_y).
        """
        px_x = ((robot_x - self.offset_x) / self.scale_x) + self.cx
        px_y = ((robot_y - self.offset_y) / self.scale_y) + self.cy
        return float(px_x), float(px_y)
