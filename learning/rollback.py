import os
import shutil
import config

class ModelRollbackManager:
    """
    Manages model version backups and rollback capabilities.
    """
    def create_backup(self):
        if os.path.exists(config.ML_MODEL_PATH):
            backup_path = config.ML_MODEL_PATH + ".bak"
            shutil.copyfile(config.ML_MODEL_PATH, backup_path)
            print("[ModelRollbackManager] Backup created.")

    def rollback(self, active_ml_predictor) -> bool:
        backup_path = config.ML_MODEL_PATH + ".bak"
        if os.path.exists(backup_path):
            shutil.copyfile(backup_path, config.ML_MODEL_PATH)
            active_ml_predictor.load_model()
            print("[ModelRollbackManager] Successfully rolled back to previous model version.")
            return True
        print("[ModelRollbackManager] No backup available for rollback.")
        return False
