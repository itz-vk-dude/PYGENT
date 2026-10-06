import unittest
from robotics.kinematics import RoboticArmKinematics

class TestKinematics(unittest.TestCase):
    def test_kinematics_fk_ik(self):
        kin = RoboticArmKinematics()
        
        # Test FK from valid joint angles
        start_j1, start_j2, start_j3, start_j4, start_j5 = 0.0, 45.0, 0.0, 0.0, 90.0
        x, y, z = kin.forward_kinematics(start_j1, start_j2, start_j3, start_j4, start_j5)
        
        # Test IK reconstruction
        j1, j2, j3, j4, j5 = kin.inverse_kinematics(x, y, z, pitch_angle_deg=45.0)
        
        self.assertTrue(0.0 <= j1 <= 180.0)
        self.assertTrue(0.0 <= j2 <= 180.0)
        self.assertTrue(0.0 <= j3 <= 180.0)
        self.assertTrue(0.0 <= j4 <= 180.0)
        self.assertTrue(0.0 <= j5 <= 180.0)

        calc_x, calc_y, calc_z = kin.forward_kinematics(j1, j2, j3, j4, j5)
        self.assertLess(abs(calc_x - x) + abs(calc_y - y) + abs(calc_z - z), 30.0)

if __name__ == "__main__":
    unittest.main()
