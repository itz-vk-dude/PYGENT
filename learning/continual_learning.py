from typing import Dict, Any
from learning.model_updater import ModelUpdater
import config

class ContinualLearningEngine:
    """
    Continual Learning Engine for PHYGENT.
    Logs verified physical experiences and periodically triggers retraining when experience threshold is reached.
    """
    def __init__(self, db_manager, active_ml_predictor):
        self.db = db_manager
        self.ml_predictor = active_ml_predictor
        self.updater = ModelUpdater()
        self.experience_counter = 0
        self.batch_size = config.CONTINUAL_LEARNING_BATCH_SIZE

    def process_experience(self, perception_data: Dict[str, Any], evaluation: Dict[str, Any]):
        if evaluation.get("status") in ("SUCCESS", "PARTIAL"):
            self.experience_counter += 1

        if self.experience_counter >= self.batch_size:
            res = self.updater.update_model(self.ml_predictor, self.db)
            print(f"[ContinualLearning] Batch retrain trigger: {res['reason']}")
            self.experience_counter = 0
