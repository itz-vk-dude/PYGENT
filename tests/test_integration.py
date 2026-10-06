import unittest
from agent.agent_core import PHYGENTAgentCore

class TestIntegration(unittest.TestCase):
    def test_full_loop_step(self):
        agent = PHYGENTAgentCore(system_mode="SIMULATION")
        agent.step()
        state = agent.state_manager.get_state()
        self.assertEqual(state["system_mode"], "SIMULATION")
        self.assertIn("robot", state)
        self.assertIn("prediction", state)
        self.assertIn("decision", state)
        self.assertIn("safety", state)

if __name__ == "__main__":
    unittest.main()
