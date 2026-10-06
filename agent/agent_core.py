import time
from typing import Dict, Any, Tuple
from physical_world.camera import CameraStream
from perception.perception_engine import PerceptionEngine
from data.quality import DataQualityChecker
from data.database import DatabaseManager
from world_model.state_manager import StateManager
from prediction.hybrid_predictor import HybridPredictor
from reasoning.reasoning_engine import ReasoningEngine
from simulation.candidate_actions import CandidateActionGenerator
from simulation.simulator import Simulator
from decision.decision_engine import DecisionEngine
from robotics.executor import ActionExecutor
from communication.serial_controller import SerialController
from communication.telemetry import TelemetryReceiver
from feedback.feedback_engine import FeedbackEngine
from learning.continual_learning import ContinualLearningEngine
from agent.context_manager import ContextManager
from agent.autonomy_manager import AutonomyManager
from agent.task_manager import TaskManager
from agent.user_profile import UserProfile
from agent.interaction_manager import InteractionManager
from interaction.conversation import ConversationEngine

class PHYGENTAgentCore:
    """
    PHYGENT Central Orchestrator & Cognitive Brain.
    Implements the core literature-survey lifecycle:
    observe -> understand -> predict -> reason -> simulate -> decide -> act -> observe_result -> evaluate -> learn.
    """
    def __init__(self, serial_port: str = "COM3", system_mode: str = "SIMULATION"):
        self.state_manager = StateManager(system_mode=system_mode)
        self.camera = CameraStream()
        self.perception_engine = PerceptionEngine()
        self.quality_checker = DataQualityChecker()
        self.db = DatabaseManager()
        self.hybrid_predictor = HybridPredictor()
        self.reasoning_engine = ReasoningEngine()
        self.action_generator = CandidateActionGenerator()
        self.simulator = Simulator()
        self.decision_engine = DecisionEngine()
        self.executor = ActionExecutor()
        self.serial_controller = SerialController(port=serial_port)
        self.telemetry_receiver = TelemetryReceiver()
        self.feedback_engine = FeedbackEngine()
        self.continual_learning = ContinualLearningEngine(self.db, self.hybrid_predictor.ml_predictor)
        
        self.context_manager = ContextManager()
        self.autonomy_manager = AutonomyManager()
        self.task_manager = TaskManager()
        self.user_profile = UserProfile()
        self.conversation = ConversationEngine(self.reasoning_engine)
        self.interaction_manager = InteractionManager(self.conversation)

        self.voice_offset = [0.0, 0.0, 0.0]
        self.dev_sim_step = 0

        if system_mode == "REAL_HARDWARE":
            self.serial_controller.connect()
            self.camera.start()

    def observe(self) -> Dict[str, Any]:
        """Step 1: PERCEPTION & CAMERA STREAM"""
        frame = self.camera.get_frame()
        if frame is None and self.state_manager.system_mode == "SIMULATION":
            # Explicitly generated frame strictly for DEVELOPMENT SIMULATION testing
            self.dev_sim_step += 1
            frame = self.camera.get_synthetic_dev_frame(self.dev_sim_step)

        raw_perception = self.perception_engine.process_frame(frame)
        self.state_manager.sync_perception(raw_perception)
        return raw_perception

    def understand(self, perception_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: DATA QUALITY & SCENE UNDERSTANDING"""
        quality = self.quality_checker.check_quality(perception_data)
        if quality["status"] == "NORMAL":
            self.db.log_trajectory(perception_data, quality["status"])
        return quality

    def predict(self, perception_data: Dict[str, Any]) -> Tuple[tuple, tuple, tuple]:
        """Step 3: HYBRID PREDICTION (ML + Physics)"""
        ml_pred, phys_pred, hybrid_pred = self.hybrid_predictor.predict(perception_data, dt=0.5)
        self.state_manager.update_predictions(ml_pred, phys_pred, hybrid_pred)
        return ml_pred, phys_pred, hybrid_pred

    def reason(self, context: Dict[str, Any]) -> str:
        """Step 4: AGENT REASONING & GROK COGNITION"""
        return "Reasoning context active."

    def simulate(self, hybrid_pred: tuple) -> list:
        """Step 5: WHAT-IF CANDIDATE ACTION SIMULATION"""
        full_st = self.state_manager.get_state()
        robot_pos = full_st["robot"]["position"]
        candidates = self.action_generator.generate_actions(hybrid_pred, robot_pos)
        sim_results = self.simulator.simulate_all(candidates, robot_pos, hybrid_pred)
        return sim_results

    def decide(self, sim_results: list, perception_data: Dict[str, Any], quality_info: Dict[str, Any]) -> Tuple[Dict[str, Any], float, str]:
        """Step 6: HARD-GATE SAFETY & ACTION DECISION"""
        human_info = perception_data.get("human_info", {})
        best_act, score, reason = self.decision_engine.select_best_action(
            sim_results, self.voice_offset, human_info, quality_info
        )
        self.state_manager.update_decision(best_act, score, reason)
        autonomy_state = self.autonomy_manager.evaluate_policy(perception_data, best_act, reason)
        self.state_manager.update_autonomy_state(autonomy_state)
        return best_act, score, reason

    def act(self, best_action: Dict[str, Any]) -> bool:
        """Step 7: PHYSICAL / SIMULATED ROBOT ACTION"""
        if self.state_manager.autonomy_state != "ACT" or best_action is None:
            return False

        success, msg = self.executor.execute_action(best_action, self.serial_controller, self.state_manager)
        return success

    def observe_result(self, hybrid_pred: tuple) -> Dict[str, Any]:
        """Step 8: REAL OBSERVATION & FEEDBACK COMPARISON (NO ARTIFICIAL OFFSETS)"""
        full_st = self.state_manager.get_state()
        raw_perception = full_st["objects"][0] if full_st["objects"] else {}
        fb_res = self.feedback_engine.process_feedback(hybrid_pred, raw_perception, full_st["robot"])
        self.db.log_feedback(hybrid_pred, fb_res["actual_pos"], fb_res["error_px"], fb_res["evaluation_status"])
        return fb_res

    def evaluate(self, fb_res: Dict[str, Any]) -> Dict[str, Any]:
        """Step 9: SELF EVALUATION"""
        return {"status": fb_res["evaluation_status"], "error_px": fb_res["error_px"]}

    def learn(self, perception_data: Dict[str, Any], eval_res: Dict[str, Any]):
        """Step 10: CONTINUAL LEARNING"""
        self.continual_learning.process_experience(perception_data, eval_res)

    def step(self):
        """Single Step Iteration of the Master Closed Loop."""
        self.telemetry_receiver.process_telemetry(self.serial_controller, self.state_manager)
        
        # 1. Observe
        perception_data = self.observe()
        
        # 2. Quality
        quality = self.understand(perception_data)
        
        # 3. Predict
        ml_pred, phys_pred, hybrid_pred = self.predict(perception_data)
        
        # 4. Simulate & Decide
        sim_results = self.simulate(hybrid_pred)
        best_act, score, reason = self.decide(sim_results, perception_data, quality)
        
        # 5. Act
        if best_act is not None and self.state_manager.autonomy_state == "ACT":
            self.act(best_act)
            
        # 6. Feedback & Learn
        fb_res = self.observe_result(hybrid_pred)
        eval_res = self.evaluate(fb_res)
        self.learn(perception_data, eval_res)
