from typing import Dict, Any

class ActionScorer:
    def __init__(self, w_error: float = 0.60, w_time: float = 0.25, w_cost: float = 0.15):
        self.w_error = w_error
        self.w_time = w_time
        self.w_cost = w_cost

    def calculate_score(self, sim_result: Dict[str, Any]) -> float:
        """
        Computes composite decision score. Lower score is better.
        Score = w_error * position_error + w_time * execution_time + w_cost * (movement_cost / 10.0)
        """
        err = sim_result.get("position_error", 0.0)
        t = sim_result.get("execution_time", 0.0)
        cost = sim_result.get("movement_cost", 0.0)

        score = (self.w_error * err) + (self.w_time * t * 10.0) + (self.w_cost * (cost / 10.0))
        return float(score)
