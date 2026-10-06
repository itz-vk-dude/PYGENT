import math
from typing import Tuple, List
import config

class RoboticArmKinematics:
    """
    5-DOF Robotic Arm Kinematics Engine.
    Calculates Forward Kinematics (FK) and Inverse Kinematics (IK)
    Link lengths:
      l1 = 100.0 mm (Base height)
      l2 = 120.0 mm (Upper arm)
      l3 = 100.0 mm (Forearm)
      l4 = 80.0 mm  (Wrist to end-effector)
    """
    def __init__(self, l1: float = None, l2: float = None, l3: float = None, l4: float = None):
        self.l1 = l1 or config.LINK_L1_BASE_HEIGHT
        self.l2 = l2 or config.LINK_L2_UPPER_ARM
        self.l3 = l3 or config.LINK_L3_FOREARM
        self.l4 = l4 or config.LINK_L4_WRIST_EE

    def forward_kinematics(self, j1: float, j2: float, j3: float, j4: float, j5: float) -> Tuple[float, float, float]:
        """
        Calculates Cartesian position (X, Y, Z) in mm given 5 joint angles in degrees.
        """
        rad_j1 = math.radians(j1)
        rad_j2 = math.radians(j2)
        rad_j3 = math.radians(j3)
        rad_j4 = math.radians(j4)

        r = (self.l2 * math.cos(rad_j2) + 
             self.l3 * math.cos(rad_j2 + rad_j3) + 
             self.l4 * math.cos(rad_j2 + rad_j3 + rad_j4))

        x = r * math.cos(rad_j1)
        y = r * math.sin(rad_j1)
        z = (self.l1 + 
             self.l2 * math.sin(rad_j2) + 
             self.l3 * math.sin(rad_j2 + rad_j3) + 
             self.l4 * math.sin(rad_j2 + rad_j3 + rad_j4))

        return round(x, 1), round(y, 1), round(z, 1)

    def inverse_kinematics(self, x: float, y: float, z: float, pitch_angle_deg: float = 45.0) -> Tuple[float, float, float, float, float]:
        """
        Calculates required 5 joint angles (J1..J5) in degrees for target Cartesian (X, Y, Z).
        Returns joint angles bounded within physical servo ranges (0° to 180°).
        """
        j1 = math.degrees(math.atan2(y, x))
        if j1 < 0:
            j1 += 360.0

        r = math.sqrt(x**2 + y**2)

        pitch_rad = math.radians(pitch_angle_deg)
        r_w = r - self.l4 * math.cos(pitch_rad)
        z_w = (z - self.l1) - self.l4 * math.sin(pitch_rad)

        d_sq = r_w**2 + z_w**2
        cos_j3 = (d_sq - self.l2**2 - self.l3**2) / (2.0 * self.l2 * self.l3)
        cos_j3 = max(-1.0, min(1.0, cos_j3))
        rad_j3 = math.acos(cos_j3)
        j3 = math.degrees(rad_j3)

        alpha = math.atan2(z_w, r_w)
        beta = math.atan2(self.l3 * math.sin(rad_j3), self.l2 + self.l3 * math.cos(rad_j3))
        j2 = math.degrees(alpha + beta)

        j4 = pitch_angle_deg - (j2 + j3)
        j5 = 90.0

        # Clamp to physical servo bounds [0, 180]
        j1_clamped = max(0.0, min(180.0, j1))
        j2_clamped = max(0.0, min(180.0, j2))
        j3_clamped = max(0.0, min(180.0, j3))
        j4_clamped = max(0.0, min(180.0, abs(j4)))
        j5_clamped = max(0.0, min(180.0, j5))

        return round(j1_clamped, 1), round(j2_clamped, 1), round(j3_clamped, 1), round(j4_clamped, 1), round(j5_clamped, 1)
