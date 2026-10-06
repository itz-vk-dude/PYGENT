import unittest
from feedback.feedback_engine import FeedbackEngine

class TestFeedback(unittest.TestCase):
    def test_feedback_engine(self):
        engine = FeedbackEngine()
        pred = (100.0, 100.0)
        perception_data = {"detected": True, "x": 105.0, "y": 98.0}
        robot_state = {"position": [100.0, 100.0, 150.0]}
        
        res = engine.process_feedback(pred, perception_data, robot_state)
        self.assertIn("error_px", res)
        self.assertGreater(res["error_px"], 0)
        self.assertIn(res["evaluation_status"], ("SUCCESS", "PARTIAL", "FAILURE"))

if __name__ == "__main__":
    unittest.main()
