import numpy as np
from sklearn.ensemble import RandomForestRegressor
from learning.validation import ModelValidator
from learning.rollback import ModelRollbackManager

class ModelUpdater:
    """
    Trains candidate ML model on accumulated verified trajectories and triggers validation.
    """
    def __init__(self):
        self.validator = ModelValidator()
        self.rollback_mgr = ModelRollbackManager()

    def update_model(self, active_ml_predictor, db_manager) -> dict:
        raw_rows = db_manager.get_all_training_data()
        if len(raw_rows) < 10:
            return {"updated": False, "reason": "Insufficient database experience records (< 10)"}

        from learning.dataset_manager import DatasetManager
        ds_mgr = DatasetManager()
        X, y = ds_mgr.prepare_dataset(raw_rows)

        if len(X) < 5:
            return {"updated": False, "reason": "Dataset preparation produced < 5 samples"}

        # Train candidate
        candidate = RandomForestRegressor(n_estimators=50, random_state=42)
        candidate.fit(X, y)

        # Validate candidate vs current active model
        val_res = self.validator.validate_candidate(active_ml_predictor, candidate, X, y)
        if val_res["accepted"]:
            self.rollback_mgr.create_backup()
            active_ml_predictor.train(X, y)
            return {"updated": True, "reason": f"Model updated successfully ({val_res['reason']})"}
        else:
            return {"updated": False, "reason": f"Candidate rejected ({val_res['reason']})"}
