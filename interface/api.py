from flask import Blueprint, jsonify, request, Response
import json
import time
import cv2

api_bp = Blueprint('api', __name__)

state_store_ref = None
agent_core_ref = None

def init_api(state_store, agent_core):
    global state_store_ref, agent_core_ref
    state_store_ref = state_store
    agent_core_ref = agent_core

@api_bp.route('/api/state', methods=['GET'])
def get_state():
    if state_store_ref:
        return jsonify(state_store_ref.get())
    return jsonify({})

@api_bp.route('/api/stream/state', methods=['GET'])
def stream_state():
    def event_stream():
        while True:
            if state_store_ref:
                data = json.dumps(state_store_ref.get())
                yield f"data: {data}\n\n"
            time.sleep(0.1)
    return Response(event_stream(), mimetype="text/event-stream")

@api_bp.route('/video_feed', methods=['GET'])
def video_feed():
    def generate_frames():
        while True:
            if agent_core_ref and agent_core_ref.camera:
                frame = agent_core_ref.camera.get_frame()
                if frame is None and agent_core_ref.state_manager.system_mode == "SIMULATION":
                    frame = agent_core_ref.camera.get_synthetic_dev_frame(int(time.time() * 10))
                
                if frame is not None:
                    # Draw workspace bounding box
                    cv2.rectangle(frame, (100, 50), (540, 430), (0, 255, 255), 2)
                    cv2.putText(frame, "PHYSICAL WORKSPACE", (105, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                    
                    ret, buffer = cv2.imencode('.jpg', frame)
                    if ret:
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.05)

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@api_bp.route('/api/conversation', methods=['POST'])
def post_conversation():
    data = request.json or {}
    text = data.get("text", "")
    if agent_core_ref and text:
        res = agent_core_ref.interaction_manager.process_voice_transcript(
            text, agent_core_ref.state_manager.get_state()
        )
        return jsonify(res)
    return jsonify({"error": "No text or agent inactive"})

@api_bp.route('/api/robot/home', methods=['POST'])
def robot_home():
    if agent_core_ref:
        agent_core_ref.serial_controller.home()
        agent_core_ref.state_manager.update_autonomy_state("OBSERVE")
        return jsonify({"status": "HOMED"})
    return jsonify({"error": "Agent inactive"})

@api_bp.route('/api/robot/stop', methods=['POST'])
def robot_stop():
    if agent_core_ref:
        agent_core_ref.serial_controller.stop()
        agent_core_ref.state_manager.update_autonomy_state("STOP")
        return jsonify({"status": "STOPPED"})
    return jsonify({"error": "Agent inactive"})

@api_bp.route('/api/robot/pause', methods=['POST'])
def robot_pause():
    if agent_core_ref:
        agent_core_ref.serial_controller.pause()
        agent_core_ref.state_manager.update_autonomy_state("PAUSE")
        return jsonify({"status": "PAUSED"})
    return jsonify({"error": "Agent inactive"})

@api_bp.route('/api/robot/resume', methods=['POST'])
def robot_resume():
    if agent_core_ref:
        agent_core_ref.serial_controller.resume()
        agent_core_ref.state_manager.update_autonomy_state("OBSERVE")
        return jsonify({"status": "RESUMED"})
    return jsonify({"error": "Agent inactive"})

@api_bp.route('/api/learning/rollback', methods=['POST'])
def learning_rollback():
    if agent_core_ref:
        from learning.rollback import ModelRollbackManager
        rb = ModelRollbackManager()
        success = rb.rollback(agent_core_ref.hybrid_predictor.ml_predictor)
        return jsonify({"status": "SUCCESS" if success else "FAILED"})
    return jsonify({"error": "Agent inactive"})
