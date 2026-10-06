import threading
import time
from typing import Dict, Any, List
from world_model.world_model import WorldModel
from world_model.synchronization import TelemetrySynchronizer
from robotics.kinematics import RoboticArmKinematics
import config

class StateManager:
    """
    Central Thread-Safe Single Source of Truth for PHYGENT System State.
    Contains PHYGENT_STATE dict structure consumed by UI, Agent, Digital Twin, Decision & Learning.
    """
    def __init__(self, system_mode: str = None):
        self.lock = threading.Lock()
        self.world = WorldModel()
        self.synchronizer = TelemetrySynchronizer()
        self.kinematics = RoboticArmKinematics()
        
        self.system_mode = system_mode if system_mode else config.DEFAULT_SYSTEM_MODE
        self.autonomy_state = "OBSERVE"
        self.current_task = {"name": "PERCEPTION_TRACKING", "status": "WAITING", "progress": 0.0}
        self.conversation_state = {"last_user": "", "last_agent": "", "state": "IDLE"}
        self.last_command = "IDLE"
        self.person_present = False
        self.objects = []
        self.humans = []
        self.prediction_data = {"ml": (0, 0), "physics": (0, 0), "hybrid": (0, 0), "confidence": 0.0}
        self.simulation_data = {"candidates_count": 0, "best_candidate": None}
        self.decision_data = {"selected_action": None, "score": 0.0, "reason": "PENDING"}
        self.safety_data = {"status": "SAFE", "hard_gate": "PASSED", "reason": "APPROVED"}
        self.learning_data = {"total_experiences": 0, "model_version": "v1.0", "validation_score": 0.95}

    def set_system_mode(self, mode: str):
        with self.lock:
            self.system_mode = mode

    def sync_perception(self, perception_data: Dict[str, Any]):
        with self.lock:
            if perception_data.get("status") == "CAMERA_OFFLINE":
                self.person_present = False
                self.objects = []
                self.humans = []
                return

            pos = [perception_data.get("x", 0.0), perception_data.get("y", 0.0), 0.0]
            vel = [perception_data.get("vx", 0.0), perception_data.get("vy", 0.0), 0.0]
            self.world.object.update_state(pos, vel, perception_data.get("radius", 15.0))
            self.person_present = perception_data.get("person_present", False)
            self.objects = perception_data.get("objects", [])
            if "human_info" in perception_data:
                self.humans = [perception_data["human_info"]]

    def sync_telemetry(self, measured_joints: List[float], hardware_connected: bool, gripper_state: str = "OPEN"):
        with self.lock:
            self.synchronizer.sync(self.world.robot, measured_joints, hardware_connected)
            if len(measured_joints) >= 5:
                x, y, z = self.kinematics.forward_kinematics(*measured_joints[:5])
                self.world.robot.update_position([x, y, z])
            self.world.robot.update_gripper(gripper_state)

    def set_commanded_joints(self, joints: List[float]):
        with self.lock:
            self.world.robot.update_commanded_joints(joints)

    def update_predictions(self, ml_pred: tuple, phys_pred: tuple, hybrid_pred: tuple, confidence: float = 0.95):
        with self.lock:
            self.prediction_data = {
                "ml": [round(ml_pred[0], 1), round(ml_pred[1], 1)],
                "physics": [round(phys_pred[0], 1), round(phys_pred[1], 1)],
                "hybrid": [round(hybrid_pred[0], 1), round(hybrid_pred[1], 1)],
                "confidence": confidence
            }

    def update_decision(self, action: Dict[str, Any], score: float, safety_reason: str):
        with self.lock:
            self.decision_data = {
                "selected_action": action,
                "score": round(score, 2),
                "reason": safety_reason
            }
            if action is None:
                self.safety_data = {"status": "REJECTED", "hard_gate": "FAILED", "reason": safety_reason}
            else:
                self.safety_data = {"status": "SAFE", "hard_gate": "PASSED", "reason": safety_reason}

    def update_autonomy_state(self, state: str):
        with self.lock:
            self.autonomy_state = state

    def get_state(self) -> Dict[str, Any]:
        with self.lock:
            full_world = self.world.get_full_state()
            
            phygent_state = {
                "system_mode": self.system_mode,
                "environment": {"light_level": "NORMAL", "workspace_occupied": self.person_present or len(self.objects) > 0},
                "humans": self.humans,
                "objects": self.objects,
                "person_present": self.person_present,
                "robot": full_world["robot"],
                "task": self.current_task,
                "prediction": self.prediction_data,
                "simulation": self.simulation_data,
                "decision": self.decision_data,
                "safety": self.safety_data,
                "conversation": self.conversation_state,
                "learning": self.learning_data,
                "agent": {
                    "autonomy_state": self.autonomy_state,
                    "last_command": self.last_command
                },
                "timestamp": time.time()
            }
            return phygent_state
