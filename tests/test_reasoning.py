import unittest
from reasoning.reasoning_engine import ReasoningEngine

class TestReasoning(unittest.TestCase):
    def test_reasoning_interaction(self):
        engine = ReasoningEngine()
        dummy_state = {"system_mode": "SIMULATION", "person_present": False, "objects": []}
        res = engine.process_natural_interaction("Hey, this side looks a little crowded.", dummy_state)
        self.assertIn("speech_response", res)
        self.assertTrue(len(res["speech_response"]) > 0)

if __name__ == "__main__":
    unittest.main()
