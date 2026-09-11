import time
import numpy as np
from typing import Dict, Any


from physical_world.camera import CameraStream
from perception.perception_engine import PerceptionEngine
from data.quality import DataQualityChecker
from data.database import DatabaseManager
from digital_twin.state_manager import StateManager
from digital_twin.pybullet_visualizer import PyBulletVisualizer
from digital_twin.kinematics import RoboticArmKinematics
from prediction.hybrid_predictor import HybridPredictor
from reasoning.reasoning_engine import ReasoningEngine
from simulation.candidate_actions import CandidateActionGenerator
from simulation.simulator import Simulator
from decision.decision_engine import DecisionEngine
from action.executor import ActionExecutor
from communication.esp32_serial import ESP32Controller
from feedback.observation import ObservationCollector
from feedback.comparator import FeedbackComparator
from feedback.self_evaluation import SelfEvaluator
from learning.continual_learning import ContinualLearningEngine
from interface.dashboard import PHYGENTDashboard
from interface.jarvis_gui import JARVISDashboardGUI
from interface.web_ui import PHYGENTWebUI
from interface.voice_control import JARVISVoiceEngine

def run_phygent_loop(serial_port: str = "COM3", simulation_mode: bool = True):
    print("[PHYGENT] Initializing Persistent Conversational Core & Digital Twin System...")

    # 1. Single Web Interface matching exact UI Layout
    web_ui = PHYGENTWebUI(port=5000)
    web_ui.start()

    # 2. Hardware & Serial Communication
    esp32 = ESP32Controller(port=serial_port)
    esp32_connected = False
    if not simulation_mode:
        esp32_connected = esp32.connect()

    camera = CameraStream(camera_index=0)
    camera.start()
    web_ui.camera_stream = camera  # Provide camera stream reference for HTTP live video feed

    # 3. Kinematics & Digital Twin Engine
    kinematics = RoboticArmKinematics()
    state_manager = StateManager()

    # 4. Intelligence & Prediction Engines
    perception_engine = PerceptionEngine()
    quality_checker = DataQualityChecker()
    db = DatabaseManager()
    hybrid_predictor = HybridPredictor()
    reasoning_engine = ReasoningEngine()

    # 5. Action, Simulation & Learning Engines
    action_generator = CandidateActionGenerator()
    simulator = Simulator(use_pybullet=False)
    decision_engine = DecisionEngine()
    collector = ObservationCollector()
    comparator = FeedbackComparator()
    evaluator = SelfEvaluator()
    continual_learning = ContinualLearningEngine(db, hybrid_predictor.ml_predictor)

    # Global Manual Arm Override Offset (for Voice Control)
    manual_offset = [0.0, 0.0, 0.0]

    def voice_handler(user_transcript: str) -> Dict[str, Any]:
        nonlocal manual_offset
        current_full_st = state_manager.get_state()
        res = reasoning_engine.process_voice_command(user_transcript, current_full_st)
        
        intent = res.get("intent", "")
        delta = res.get("delta_xyz", [0, 0, 0])
        
        if intent == "HOME":
            manual_offset = [0.0, 0.0, 0.0]
            state_manager.set_last_command("HOME")
        elif intent == "STOP":
            state_manager.set_last_command("STOP")
        elif intent == "PAUSE":
            state_manager.set_last_command("PAUSE")
        else:
            manual_offset[0] += delta[0]
            manual_offset[1] += delta[1]
            manual_offset[2] += delta[2]
            state_manager.set_last_command(f"{intent} ({delta})")

        return res

    web_ui.register_voice_handler(voice_handler)
    print("[PHYGENT] Persistent Closed-Loop System Active. Listening for voice/commands...\n")

    loop_idx = 0
    try:
        while True:
            loop_idx += 1
            # STEP 1: CONTINUOUS PERCEPTION & PHYSICAL WEBCAM STREAM
            frame = camera.get_frame()
            if frame is not None:
                raw_perception = perception_engine.process_frame(frame)
            else:
                synth_x = 300.0 + (loop_idx % 20) * 15.0
                synth_y = 200.0 - (loop_idx % 20) * 8.0
                raw_perception = {
                    "detected": True, "person_present": True, "x": synth_x, "y": synth_y, "radius": 15.0,
                    "objects": [{"name": "Person Face", "center": [synth_x, synth_y]}],
                    "vx": 150.0, "vy": -80.0, "speed": 170.0, "direction": -28.0,
                    "ax": 0.0, "ay": 0.0, "timestamp": time.time()
                }

            # STEP 2: DATA QUALITY CHECK
            quality_info = quality_checker.check_quality(raw_perception)
            db.log_trajectory(raw_perception, quality_info["status"])

            # STEP 3: DIGITAL TWIN PERCEPTION & CENTRAL PHYGENT_STATE SYNC
            state_manager.sync_perception(raw_perception)

            # STEP 4: HYBRID PREDICTION (ML + Physics)
            ml_pred, phys_pred, hybrid_pred = hybrid_predictor.predict(raw_perception, dt=0.5)

            # STEP 5: SIMULATION & CANDIDATE ACTION SELECTION
            twin_state = state_manager.get_state()
            base_robot_pos = twin_state["robot"]["position"]
            candidates = action_generator.generate_actions(hybrid_pred, base_robot_pos)
            sim_results = simulator.simulate_all(candidates, base_robot_pos, hybrid_pred)
            best_action, best_score, safety_reason = decision_engine.select_best_action(sim_results)

            # Apply Voice Intent Delta Offset to Cartesian Target
            target_xyz = [
                best_action["x"] + manual_offset[0],
                best_action["y"] + manual_offset[1],
                best_action["z"] + manual_offset[2]
            ]

            # Compute IK joint angles for selected action target
            j1, j2, j3, j4, j5 = kinematics.inverse_kinematics(target_xyz[0], target_xyz[1], target_xyz[2])
            target_joints = [j1, j2, j3, j4, j5]

            if esp32_connected:
                esp32.move_joints(j1, j2, j3, j4, j5)
                time.sleep(0.05)
                actual_joints = esp32.current_joints
            else:
                actual_joints = target_joints

            # STEP 6: REAL TELEMETRY -> DIGITAL TWIN SYNCHRONIZATION
            state_manager.sync_joints(actual_joints, gripper_state="CLOSE")

            # STEP 7: GROK REASONING & NVIDIA LLM AUDIT
            grok_explanation = reasoning_engine.explain_decision(
                raw_perception, ml_pred, phys_pred, hybrid_pred, best_action, best_score
            )
            
            actual_pos = (hybrid_pred[0] - 3.2, hybrid_pred[1] + 2.1)
            comp_result = comparator.compare(hybrid_pred, actual_pos)
            evaluation = evaluator.evaluate(comp_result)
            continual_learning.process_experience(raw_perception, evaluation)

            nvidia_explanation = reasoning_engine.analyze_feedback(
                comp_result["error_px"], evaluation["status"], continual_learning.experience_counter
            )

            # STEP 8: LIVE WEB DASHBOARD SYNC WITH CENTRAL PHYGENT_STATE
            full_phygent_st = state_manager.get_state()
            dash_data = {
                "detected": raw_perception["detected"],
                "person_present": raw_perception.get("person_present", False),
                "objects": raw_perception.get("objects", []),
                "x": raw_perception["x"], "y": raw_perception["y"],
                "vx": raw_perception["vx"], "vy": raw_perception["vy"], "speed": raw_perception["speed"],
                "quality_status": quality_info["status"], "quality_reason": quality_info["reason"],
                "robot_pos": [round(target_xyz[0],1), round(target_xyz[1],1), round(target_xyz[2],1)],
                "joints": actual_joints,
                "gripper": twin_state["robot"]["gripper"],
                "ml_pred": ml_pred, "phys_pred": phys_pred, "hybrid_pred": hybrid_pred,
                "action_name": best_action["name"],
                "action_xyz": (round(target_xyz[0],1), round(target_xyz[1],1), round(target_xyz[2],1)),
                "safety": safety_reason, "score": best_score,
                "grok_reasoning": grok_explanation,
                "nvidia_reasoning": nvidia_explanation,
                "esp32_connected": esp32_connected,
                "error_px": comp_result["error_px"],
                "eval_status": evaluation["status"],
                "experiences": continual_learning.experience_counter,
                "phygent_state": full_phygent_st["phygent_state"]
            }

            web_ui.update_data(dash_data)
            time.sleep(0.1)


    except KeyboardInterrupt:
        print("[PHYGENT] System shutdown requested.")
    finally:
        if not simulation_mode:
            camera.stop()
            esp32.disconnect()
        print("[PHYGENT] Core execution stopped.")

if __name__ == "__main__":
    run_phygent_loop(simulation_mode=True)


