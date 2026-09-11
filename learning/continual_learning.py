from data.database import DatabaseManager
from prediction.ml_model import MLPredictor
from learning.dataset_manager import DatasetManager
from learning.model_updater import ModelUpdater
from typing import Dict, Any

class ContinualLearningEngine:
    def __init__(self, db_manager: DatabaseManager, ml_predictor: MLPredictor):
        self.dataset_manager = DatasetManager(db_manager)
        self.updater = ModelUpdater(ml_predictor)
        self.experience_counter = 0

    def process_experience(self, clean_state: Dict[str, Any], evaluation_result: Dict[str, Any]):
        """
        Logs validated physical experience and triggers online model update periodically.
        """
        self.experience_counter += 1
        
        if self.experience_counter % 10 == 0:
            X, y = self.dataset_manager.prepare_training_matrices()
            self.updater.retrain_model(X, y)
