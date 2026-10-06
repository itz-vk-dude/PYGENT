import unittest
import numpy as np
from perception.perception_engine import PerceptionEngine

class TestPerception(unittest.TestCase):
    def test_perception_offline(self):
        engine = PerceptionEngine()
        res = engine.process_frame(None)
        self.assertEqual(res["status"], "CAMERA_OFFLINE")
        self.assertFalse(res["detected"])

    def test_perception_dev_frame(self):
        engine = PerceptionEngine()
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        res = engine.process_frame(frame)
        self.assertEqual(res["status"], "ONLINE")
        self.assertIn("x", res)
        self.assertIn("y", res)

if __name__ == "__main__":
    unittest.main()
