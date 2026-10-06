from typing import Dict, Any

class ActionScorer:
    """
    Multi-Factor Action Scorer.
    Calculates cost score balancing prediction error, movement distance, execution time, and safety margins.
    """
    def __init__(self, error_weight: float = 2.0, time_weight: float = 1.0, distance_weight: float = 0.5):
        self.error_weight = error_weight
        self.time_weight = time_weight
        self.distance_weight = distance_weight

    def calculate_score(self, sim_result: Dict[str, Any]) -> float:
        error = sim_result.get("predicted_error", 5.0)
        time_sec = sim_result.get("estimated_time", 1.0)
        dist = sim_result.get("distance", 100.0)

        score = (self.error_weight * error) + (self.time_weight * time_sec) + (self.distance_weight * (dist / 10.0))
        return float(score)
