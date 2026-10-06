from typing import Dict, Any, Tuple
from feedback.observation import ObservationCollector
from feedback.comparator import FeedbackComparator
from feedback.evaluator import SelfEvaluator

class FeedbackEngine:
    """
    Public Entry Point for PHYGENT Feedback Subsystem.
    Processes real camera/telemetry observations, computes position errors, and evaluates performance.
    """
    def __init__(self):
        self.collector = ObservationCollector()
        self.comparator = FeedbackComparator()
        self.evaluator = SelfEvaluator()

    def process_feedback(self, predicted_pos: Tuple[float, float], perception_data: Dict[str, Any], robot_state: Dict[str, Any]) -> Dict[str, Any]:
        actual_pos = self.collector.get_real_observation(perception_data, robot_state)
        comp = self.comparator.compare(predicted_pos, actual_pos)
        eval_res = self.evaluator.evaluate(comp)

        return {
            "predicted_pos": predicted_pos,
            "actual_pos": actual_pos,
            "error_px": comp["error_px"],
            "evaluation_status": eval_res["status"],
            "score": eval_res["score"]
        }
