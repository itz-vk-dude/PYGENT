import unittest
from prediction.hybrid_predictor import HybridPredictor

class TestPrediction(unittest.TestCase):
    def test_hybrid_predictor(self):
        predictor = HybridPredictor()
        dummy_state = {"x": 100.0, "y": 100.0, "vx": 10.0, "vy": -5.0}
        ml, phys, hybrid = predictor.predict(dummy_state, dt=0.5)
        self.assertEqual(len(ml), 2)
        self.assertEqual(len(phys), 2)
        self.assertEqual(len(hybrid), 2)
        self.assertAlmostEqual(hybrid[0], 0.5 * ml[0] + 0.5 * phys[0], places=4)

if __name__ == "__main__":
    unittest.main()
