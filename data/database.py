import sqlite3
import os
import time
from typing import Dict, Any, List

class DatabaseManager:
    def __init__(self, db_path: str = r"C:\PYGENT\data\phygent.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trajectory_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    x REAL,
                    y REAL,
                    vx REAL,
                    vy REAL,
                    speed REAL,
                    direction REAL,
                    ax REAL,
                    ay REAL,
                    quality_status TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS decision_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    ml_pred_x REAL,
                    ml_pred_y REAL,
                    phys_pred_x REAL,
                    phys_pred_y REAL,
                    hybrid_pred_x REAL,
                    hybrid_pred_y REAL,
                    selected_action TEXT,
                    target_x REAL,
                    target_y REAL,
                    target_z REAL,
                    grok_explanation TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    predicted_x REAL,
                    predicted_y REAL,
                    actual_x REAL,
                    actual_y REAL,
                    position_error REAL,
                    result_status TEXT
                )
            """)
            conn.commit()

    def log_trajectory(self, data: Dict[str, Any], quality_status: str = "NORMAL"):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO trajectory_data (timestamp, x, y, vx, vy, speed, direction, ax, ay, quality_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("timestamp", time.time()),
                data.get("x", 0.0), data.get("y", 0.0),
                data.get("vx", 0.0), data.get("vy", 0.0),
                data.get("speed", 0.0), data.get("direction", 0.0),
                data.get("ax", 0.0), data.get("ay", 0.0),
                quality_status
            ))
            conn.commit()

    def log_decision(self, ml_pred: tuple, phys_pred: tuple, hybrid_pred: tuple, action: dict, explanation: str = ""):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO decision_logs (timestamp, ml_pred_x, ml_pred_y, phys_pred_x, phys_pred_y, 
                                          hybrid_pred_x, hybrid_pred_y, selected_action, target_x, target_y, target_z, grok_explanation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                time.time(),
                ml_pred[0], ml_pred[1],
                phys_pred[0], phys_pred[1],
                hybrid_pred[0], hybrid_pred[1],
                str(action.get("name", "INTERCEPT")),
                action.get("x", 0.0), action.get("y", 0.0), action.get("z", 0.0),
                explanation
            ))
            conn.commit()

    def log_feedback(self, pred: tuple, actual: tuple, error: float, result_status: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback_logs (timestamp, predicted_x, predicted_y, actual_x, actual_y, position_error, result_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                time.time(), pred[0], pred[1], actual[0], actual[1], error, result_status
            ))
            conn.commit()

    def get_all_training_data(self) -> List[tuple]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT x, y, vx, vy, speed, direction, ax, ay FROM trajectory_data WHERE quality_status = 'NORMAL'")
            return cursor.fetchall()
