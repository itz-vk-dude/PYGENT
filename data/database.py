import sqlite3
import os
import time
import json
from typing import Dict, Any, List, Optional
import config

class DatabaseManager:
    """
    SQLite Audit Trail Database Manager for PHYGENT.
    Maintains 18 relational tables for complete research reproducibility.
    """
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or config.DATABASE_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE,
                    name TEXT,
                    preferred_language TEXT DEFAULT 'Tanglish',
                    created_at REAL
                )
            """)

            # 2. conversations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT UNIQUE,
                    user_id TEXT,
                    started_at REAL,
                    status TEXT
                )
            """)

            # 3. messages
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    timestamp REAL,
                    sender TEXT,
                    text TEXT,
                    intent TEXT,
                    payload TEXT
                )
            """)

            # 4. observations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    source TEXT,
                    status TEXT,
                    data_json TEXT
                )
            """)

            # 5. objects
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS objects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    object_name TEXT,
                    center_x REAL,
                    center_y REAL,
                    radius REAL,
                    confidence REAL
                )
            """)

            # 6. trajectories
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trajectories (
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

            # 7. robot_states
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS robot_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    j1 REAL, j2 REAL, j3 REAL, j4 REAL, j5 REAL,
                    pos_x REAL, pos_y REAL, pos_z REAL,
                    gripper TEXT,
                    status TEXT
                )
            """)

            # 8. robot_commands
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS robot_commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    command_type TEXT,
                    target_joints TEXT,
                    target_xyz TEXT,
                    status TEXT
                )
            """)

            # 9. robot_telemetry
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS robot_telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    source TEXT,
                    measured_joints TEXT,
                    measured_xyz TEXT,
                    status TEXT
                )
            """)

            # 10. predictions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    ml_x REAL, ml_y REAL,
                    phys_x REAL, phys_y REAL,
                    hybrid_x REAL, hybrid_y REAL,
                    confidence REAL
                )
            """)

            # 11. candidate_actions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS candidate_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    candidates_json TEXT,
                    selected_candidate TEXT
                )
            """)

            # 12. decisions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    action_name TEXT,
                    target_xyz TEXT,
                    score REAL,
                    safety_status TEXT,
                    grok_reasoning TEXT
                )
            """)

            # 13. safety_events
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS safety_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    event_type TEXT,
                    rule_triggered TEXT,
                    decision TEXT,
                    details TEXT
                )
            """)

            # 14. feedback
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    pred_x REAL, pred_y REAL,
                    actual_x REAL, actual_y REAL,
                    position_error REAL,
                    status TEXT
                )
            """)

            # 15. evaluations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evaluations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    evaluation_status TEXT,
                    score REAL,
                    details TEXT
                )
            """)

            # 16. learning_experiences
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_experiences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    experience_data TEXT,
                    quality TEXT,
                    used_for_training INTEGER DEFAULT 0
                )
            """)

            # 17. model_versions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    version TEXT,
                    metrics_json TEXT,
                    is_active INTEGER DEFAULT 0
                )
            """)

            # 18. system_events
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    subsystem TEXT,
                    event_type TEXT,
                    status TEXT,
                    message TEXT
                )
            """)

            conn.commit()

    def log_trajectory(self, data: Dict[str, Any], quality_status: str = "NORMAL"):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO trajectories (timestamp, x, y, vx, vy, speed, direction, ax, ay, quality_status)
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
                INSERT INTO decisions (timestamp, action_name, target_xyz, score, safety_status, grok_reasoning)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                time.time(),
                str(action.get("name", "NO_ACTION")),
                json.dumps(action.get("target_xyz", [action.get("x",0), action.get("y",0), action.get("z",0)])),
                action.get("score", 0.0),
                action.get("safety", "PENDING"),
                explanation
            ))
            cursor.execute("""
                INSERT INTO predictions (timestamp, ml_x, ml_y, phys_x, phys_y, hybrid_x, hybrid_y, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                time.time(),
                ml_pred[0], ml_pred[1],
                phys_pred[0], phys_pred[1],
                hybrid_pred[0], hybrid_pred[1],
                0.95
            ))
            conn.commit()

    def log_feedback(self, pred: tuple, actual: tuple, error: float, status: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback (timestamp, pred_x, pred_y, actual_x, actual_y, position_error, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                time.time(), pred[0], pred[1], actual[0], actual[1], error, status
            ))
            conn.commit()

    def log_system_event(self, subsystem: str, event_type: str, status: str, message: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO system_events (timestamp, subsystem, event_type, status, message)
                VALUES (?, ?, ?, ?, ?)
            """, (
                time.time(), subsystem, event_type, status, message
            ))
            conn.commit()

    def get_all_training_data(self) -> List[tuple]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT x, y, vx, vy, speed, direction, ax, ay FROM trajectories WHERE quality_status = 'NORMAL'")
            return cursor.fetchall()
