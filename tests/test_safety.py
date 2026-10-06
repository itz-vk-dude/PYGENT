import unittest
from decision.safety import SafetyValidator
from decision.decision_engine import DecisionEngine

class TestSafety(unittest.TestCase):
    def test_safety_bounds(self):
        validator = SafetyValidator()
        is_safe, reason = validator.validate_final_target([999.0, 100.0, 100.0])
        self.assertFalse(is_safe)
        self.assertIn("out of workspace bounds", reason)

    def test_zero_unsafe_fallback(self):
        engine = DecisionEngine()
        unsafe_candidates = [{
            "action": {"name": "UNSAFE_INTERCEPT", "target_xyz": [999.0, 999.0, 999.0], "x": 999.0, "y": 999.0, "z": 999.0},
            "predicted_error": 5.0,
            "estimated_time": 1.0,
            "distance": 500.0
        }]
        best_act, score, reason = engine.select_best_action(unsafe_candidates)
        self.assertIsNone(best_act)
        self.assertIn("NO_SAFE_ACTION", reason)

if __name__ == "__main__":
    unittest.main()
