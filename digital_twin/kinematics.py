import math
from typing import Tuple, List

class RoboticArmKinematics:
    """
    5-DOF Robotic Arm Kinematics Engine
    Calculates Forward Kinematics (FK) and Inverse Kinematics (IK)
    Link lengths:
      l1 = 100.0 mm (Base height)
      l2 = 120.0 mm (Upper arm)
      l3 = 100.0 mm (Forearm)
      l4 = 80.0 mm  (Wrist to end-effector)
    """
    def __init__(self, l1: float = 100.0, l2: float = 120.0, l3: float = 100.0, l4: float = 80.0):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4 = l4

    def forward_kinematics(self, j1: float, j2: float, j3: float, j4: float, j5: float) -> Tuple[float, float, float]:
        """
        Calculates Cartesian position (X, Y, Z) in mm given 5 joint angles in degrees.
        J1: Base rotation angle (yaw)
        J2: Shoulder pitch angle
        J3: Elbow pitch angle
        J4: Wrist pitch angle
        J5: Wrist roll angle
        """
        rad_j1 = math.radians(j1)
        rad_j2 = math.radians(j2)
        rad_j3 = math.radians(j3)
        rad_j4 = math.radians(j4)

        # Planar reach along arm axis
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

    def inverse_kinematics(self, x: float, y: float, z: float, pitch_angle_deg: float = 0.0) -> Tuple[float, float, float, float, float]:
        """
        Calculates required 5 joint angles (J1..J5) in degrees for target Cartesian (X, Y, Z).
        Returns joint angles bounded within safe physical servo ranges (0° to 180°).
        """
        # J1: Base angle around Z axis
        j1 = math.degrees(math.atan2(y, x))

        # Project reach onto XY plane
        r = math.sqrt(x**2 + y**2)

        # Target wrist location (subtract wrist link l4)
        pitch_rad = math.radians(pitch_angle_deg)
        r_w = r - self.l4 * math.cos(pitch_rad)
        z_w = (z - self.l1) - self.l4 * math.sin(pitch_rad)

        # 2-link planar IK for Shoulder (l2) & Elbow (l3)
        d_sq = r_w**2 + z_w**2
        d = math.sqrt(d_sq)

        # Law of cosines for elbow angle J3
        cos_j3 = (d_sq - self.l2**2 - self.l3**2) / (2.0 * self.l2 * self.l3)
        cos_j3 = max(-1.0, min(1.0, cos_j3))  # Clamp to valid domain
        rad_j3 = math.acos(cos_j3)
        j3 = math.degrees(rad_j3)

        # Shoulder angle J2
        alpha = math.atan2(z_w, r_w)
        beta = math.atan2(self.l3 * math.sin(rad_j3), self.l2 + self.l3 * math.cos(rad_j3))
        j2 = math.degrees(alpha + beta)

        # Wrist pitch angle J4
        j4 = pitch_angle_deg - (j2 + j3)
        j5 = 90.0  # Default neutral wrist roll

        # Normalize and clamp servo angles between 0° and 180°
        j1_clamped = max(0.0, min(180.0, (j1 + 180) % 180 if j1 < 0 else j1))
        j2_clamped = max(0.0, min(180.0, abs(j2)))
        j3_clamped = max(0.0, min(180.0, abs(j3)))
        j4_clamped = max(0.0, min(180.0, abs(j4)))
        j5_clamped = max(0.0, min(180.0, j5))

        return round(j1_clamped, 1), round(j2_clamped, 1), round(j3_clamped, 1), round(j4_clamped, 1), round(j5_clamped, 1)
