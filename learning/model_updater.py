from prediction.ml_model import MLPredictor
import numpy as np

class ModelUpdater:
    def __init__(self, ml_predictor: MLPredictor):
        self.ml_predictor = ml_predictor

    def retrain_model(self, X: np.ndarray, y: np.ndarray) -> bool:
        if len(X) >= 5:
            self.ml_predictor.train(X, y)
            print(f"[ModelUpdater] Online retraining completed with {len(X)} samples.")
            return True
        return False
