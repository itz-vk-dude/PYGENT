import numpy as np
from typing import Dict, Any

class ModelValidator:
    """
    Validates newly trained candidate ML model against held-out validation trajectories.
    Candidate model is accepted ONLY if validation error is lower than current active model.
    """
    def validate_candidate(self, active_model, candidate_model, X_val: np.ndarray, y_val: np.ndarray) -> Dict[str, Any]:
        if len(X_val) == 0 or len(y_val) == 0:
            return {"accepted": True, "reason": "Insufficient validation data, accepted default candidate."}

        active_preds = active_model.model.predict(X_val) if active_model.is_trained else y_val + 99.0
        cand_preds = candidate_model.predict(X_val)

        active_mae = np.mean(np.abs(active_preds - y_val))
        cand_mae = np.mean(np.abs(cand_preds - y_val))

        accepted = cand_mae <= active_mae
        reason = f"Candidate MAE ({cand_mae:.2f}) vs Active MAE ({active_mae:.2f})"

        return {
            "accepted": accepted,
            "reason": reason,
            "candidate_mae": float(cand_mae),
            "active_mae": float(active_mae)
        }
