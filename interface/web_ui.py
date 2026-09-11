import os
import json
import threading
import time
from flask import Flask, render_template_string, jsonify, request
from typing import Dict, Any

class PHYGENTWebUI:
    """
    Futuristic Web-based Dashboard matching exact JARVIS layout:
    - Sidebar Navigation (Perception, Prediction, Digital Twin, AI Reasoning, Simulation, Decision, etc.)
    - Glowing Core Orb (PHYGENT Hybrid Intelligence Core with animated node status)
    - 3D Robotic Arm View Canvas (Three.js 5-DOF arm rendering with Live Sync)
    - Grok LLM Reasoning Box + NVIDIA Build LLM Audit Box
    - Live Camera Feed + Trajectory Prediction Graph
    - System Status Check & Mode Switchers
    - Voice Interaction HUD
    """
    def __init__(self, port: int = 5000):
        self.port = port
        self.app = Flask(__name__)
        self.current_data: Dict[str, Any] = {
            "detected": True, "x": 315.0, "y": 192.0, "speed": 170.0, "vx": 150.0, "vy": -80.0,
            "quality_status": "NORMAL", "robot_pos": [135.0, 6.0, 150.0],
            "joints": [90.0, 45.0, 45.0, 30.0, 10.0], "gripper": "OPEN",
            "ml_pred": (390.0, 152.0), "phys_pred": (390.0, 152.0), "hybrid_pred": (390.0, 152.0),
            "action_name": "DIRECT INTERCEPT", "score": 5.55, "safety": "APPROVED",
            "grok_reasoning": "The detected object is moving towards the right with a speed of 170 px/s. Based on trajectory prediction and current arm position, a direct intercept is the most efficient action. Safety constraints are satisfied.",
            "nvidia_reasoning": "The system performance is within expected range. Error rate: 3.8 px. The latest experience has been stored for continual learning. No anomalies detected. Recommendation: Continue current strategy and refine model with new data.",
            "esp32_connected": False, "error_px": 3.8, "eval_status": "SUCCESS", "experiences": 1
        }
        self.voice_handler = None
        self.setup_routes()
        self.server_thread = None

    def register_voice_handler(self, handler_fn):
        self.voice_handler = handler_fn

    def setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template_string(HTML_TEMPLATE)

        @self.app.route("/video_feed")
        def video_feed():
            def generate():
                import cv2
                while True:
                    if hasattr(self, 'camera_stream') and self.camera_stream:
                        frame = self.camera_stream.get_frame()
                        if frame is not None:
                            ret, jpeg = cv2.imencode('.jpg', frame)
                            if ret:
                                yield (b'--frame\r\n'
                                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
                    time.sleep(0.04)
            from flask import Response
            return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


        @self.app.route("/api/data")
        def get_data():
            return jsonify(self.current_data)

        @self.app.route("/api/voice_command", methods=["POST"])
        def handle_voice():
            payload = request.json or {}
            transcript = payload.get("transcript", "")
            if self.voice_handler and transcript:
                res = self.voice_handler(transcript)
                return jsonify(res)
            return jsonify({"speech_response": "Hello pa, naan ketkuren sollunga!", "intent": "NONE"})

        @self.app.route("/api/system_control", methods=["POST"])
        def handle_system_control():
            payload = request.json or {}
            action = payload.get("action", "").upper()
            if self.voice_handler:
                if action == "STOP":
                    res = self.voice_handler("stop")
                    res["speech_response"] = "System stop pantaen pa! Arm emergency freeze-la irukku."
                elif action == "PAUSE":
                    res = self.voice_handler("pause")
                    res["speech_response"] = "System pause pantaen pa. Resume panna thirumba press pannunga."
                elif action == "HOME":
                    res = self.voice_handler("home")
                    res["speech_response"] = "Robo arm home position-ukku vanthuruchu pa!"
                else:
                    res = self.voice_handler(action.lower())
                return jsonify(res)
            return jsonify({"speech_response": f"Command {action} executed.", "intent": action})



    def start(self):
        def _run():
            self.app.run(host="127.0.0.1", port=self.port, debug=False, use_reloader=False)

        self.server_thread = threading.Thread(target=_run, daemon=True)
        self.server_thread.start()
        print(f"[PHYGENT Web UI] Serving futuristic interface at http://127.0.0.1:{self.port}")

        def _launch_browser():
            time.sleep(1.2)
            try:
                import webview
                webview.create_window('PHYGENT — Hybrid Intelligence Core', f'http://127.0.0.1:{self.port}', width=1440, height=900)
                webview.start()
            except Exception as e:
                import webbrowser
                webbrowser.open(f'http://127.0.0.1:{self.port}')

        threading.Thread(target=_launch_browser, daemon=True).start()

    def update_data(self, data: Dict[str, Any]):
        self.current_data.update(data)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PHYGENT — Hybrid Intelligence Core</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #040814;
            --panel-bg: rgba(10, 20, 40, 0.75);
            --border-cyan: #00E5FF;
            --border-dim: rgba(0, 229, 255, 0.25);
            --neon-green: #00FF66;
            --neon-orange: #FF6600;
            --text-main: #D0E4FF;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Rajdhani', sans-serif; user-select: none; }
        body { background: var(--bg-dark); color: var(--text-main); overflow: hidden; width: 100vw; height: 100vh; }
        
        /* Layout Grid */
        .app-container {
            display: grid;
            grid-template-columns: 240px 1fr 480px;
            grid-template-rows: 60px 1fr 180px 70px;
            gap: 10px;
            padding: 10px;
            width: 100vw;
            height: 100vh;
            background: radial-gradient(circle at 50% 50%, #0a1832 0%, #030712 100%);
        }

        /* Top Header */
        header {
            grid-column: 1 / -1;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            background: var(--panel-bg);
            border: 1px solid var(--border-dim);
            box-shadow: 0 0 15px rgba(0,229,255,0.1);
        }
        .logo-title { display: flex; align-items: center; gap: 15px; font-family: 'Orbitron', sans-serif; }
        .logo-title h1 { font-size: 26px; letter-spacing: 3px; color: #FFF; text-shadow: 0 0 10px var(--border-cyan); }
        .tagline { font-size: 11px; color: var(--border-cyan); letter-spacing: 2px; }
        .flow-stepper { display: flex; gap: 15px; font-size: 12px; font-weight: 700; letter-spacing: 2px; color: #567; }
        .flow-stepper span.active { color: var(--border-cyan); text-shadow: 0 0 8px var(--border-cyan); }

        /* Left Navigation Sidebar */
        nav.sidebar {
            grid-row: 2 / 5;
            background: var(--panel-bg);
            border: 1px solid var(--border-dim);
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding: 10px 5px;
        }
        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 15px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1.5px;
            color: #789;
            border-left: 3px solid transparent;
            cursor: pointer;
            transition: 0.2s;
        }
        .nav-item.active, .nav-item:hover {
            color: #FFF;
            background: rgba(0, 229, 255, 0.1);
            border-left-color: var(--border-cyan);
            text-shadow: 0 0 8px var(--border-cyan);
        }

        /* Center Orb Visualizer Panel */
        .center-core {
            grid-column: 2;
            grid-row: 2;
            position: relative;
            background: var(--panel-bg);
            border: 1px solid var(--border-dim);
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            overflow: hidden;
        }
        .orb-ring {
            width: 320px;
            height: 320px;
            border-radius: 50%;
            border: 2px dashed var(--border-cyan);
            position: absolute;
            animation: spin 20s linear infinite;
            box-shadow: 0 0 30px rgba(0, 229, 255, 0.3);
        }
        @keyframes spin { 100% { transform: rotate(360deg); } }
        .orb-center {
            width: 240px;
            height: 240px;
            border-radius: 50%;
            background: radial-gradient(circle, #00e5ff 0%, #004488 60%, transparent 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 50px var(--border-cyan);
            animation: pulse 3s ease-in-out infinite alternate;
        }
        @keyframes pulse { 0% { transform: scale(0.95); opacity: 0.8; } 100% { transform: scale(1.05); opacity: 1.0; } }
        .orb-title { font-family: 'Orbitron'; font-size: 28px; font-weight: 900; color: #FFF; letter-spacing: 4px; text-shadow: 0 0 15px #000; }
        .orb-sub { font-size: 11px; letter-spacing: 2px; color: #000; font-weight: 800; background: var(--border-cyan); padding: 2px 8px; border-radius: 4px; }

        /* Nodes surrounding Orb */
        .node-tag {
            position: absolute;
            padding: 6px 12px;
            background: rgba(4, 12, 28, 0.85);
            border: 1px solid var(--border-cyan);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            border-radius: 4px;
        }
        .node-real { top: 20px; left: 30px; }
        .node-twin { top: 20px; right: 30px; }
        .node-ai { top: 140px; left: 10px; }
        .node-robot { top: 140px; right: 10px; }
        .node-learn { bottom: 30px; left: 40px; }
        .node-safe { bottom: 30px; right: 40px; }

        /* Right 3D Digital Twin View */
        .digital-twin-panel {
            grid-column: 3;
            grid-row: 2;
            background: var(--panel-bg);
            border: 1px solid var(--border-dim);
            position: relative;
            display: flex;
            flex-direction: column;
        }
        .panel-header {
            padding: 10px 15px;
            background: rgba(0, 229, 255, 0.08);
            border-bottom: 1px solid var(--border-dim);
            font-family: 'Orbitron';
            font-size: 14px;
            font-weight: 700;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        #canvas3d { width: 100%; height: 100%; }
        .xyz-hud {
            position: absolute;
            top: 55px; left: 15px;
            background: rgba(4, 12, 28, 0.85);
            border: 1px solid var(--border-dim);
            padding: 8px 12px;
            font-size: 12px;
            line-height: 1.6;
        }
        .joints-hud {
            position: absolute;
            top: 150px; left: 15px;
            background: rgba(4, 12, 28, 0.85);
            border: 1px solid var(--border-dim);
            padding: 8px 12px;
            font-size: 12px;
            line-height: 1.5;
        }

        /* Dual LLM Cards Panel */
        .llm-container {
            grid-column: 2;
            grid-row: 3;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .llm-card {
            background: var(--panel-bg);
            border: 1px solid var(--border-dim);
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .card-hdr { display: flex; justify-content: space-between; font-size: 13px; font-weight: 800; letter-spacing: 1px; }
        .grok-hdr { color: var(--border-cyan); }
        .nvidia-hdr { color: var(--neon-green); }
        .card-body { font-size: 12px; color: #ABC; line-height: 1.4; height: 90px; overflow-y: auto; }

        /* Bottom Right Camera & Graph Grid */
        .bottom-right-grid {
            grid-column: 3;
            grid-row: 3;
            display: grid;
            grid-template-columns: 1fr 1fr 120px;
            gap: 8px;
        }
        .mini-card {
            background: var(--panel-bg);
            border: 1px solid var(--border-dim);
            padding: 8px;
            font-size: 11px;
        }
        .cam-feed { width: 100%; height: 90px; background: #000; position: relative; border: 1px solid #345; display: flex; justify-content: center; align-items: center; }
        .cam-ball { width: 24px; height: 24px; background: var(--neon-orange); border-radius: 50%; box-shadow: 0 0 10px var(--neon-orange); }

        /* Voice Controls Bar */
        .voice-hud {
            grid-column: 2;
            grid-row: 4;
            background: var(--panel-bg);
            border: 1px solid var(--border-dim);
            display: flex;
            align-items: center;
            padding: 0 20px;
            gap: 20px;
        }
        .mic-btn { width: 42px; height: 42px; border-radius: 50%; background: var(--border-cyan); display: flex; justify-content: center; align-items: center; box-shadow: 0 0 15px var(--border-cyan); }

        /* System Action Controls */
        .system-controls {
            grid-column: 3;
            grid-row: 4;
            display: flex;
            align-items: center;
            gap: 10px;
            justify-content: flex-end;
        }
        .btn-ctrl { padding: 10px 18px; border: 1px solid var(--border-cyan); background: rgba(0, 229, 255, 0.1); color: #FFF; font-weight: 700; cursor: pointer; }
        .btn-stop { border-color: #FF2255; background: rgba(255,34,85,0.2); }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Top Header -->
        <header>
            <div class="logo-title">
                <h1>PHYGENT</h1>
                <span class="tagline">PHYSICAL INTELLIGENCE. REAL IMPACT.</span>
            </div>
            <div class="flow-stepper">
                <span class="active">SEE</span> &gt;
                <span class="active">PREDICT</span> &gt;
                <span class="active">REASON</span> &gt;
                <span class="active">ACT</span> &gt;
                <span class="active">LEARN</span>
            </div>
            <div>
                <span style="color: var(--neon-green)">● SYSTEM ACTIVE</span>
            </div>
        </header>

        <!-- Sidebar Navigation -->
        <nav class="sidebar">
            <div class="nav-item active" onclick="selectTab(this, 'HOME')">🏠 HOME</div>
            <div class="nav-item" onclick="selectTab(this, 'PERCEPTION')">👁 PERCEPTION</div>
            <div class="nav-item" onclick="selectTab(this, 'PREDICTION')">📊 PREDICTION</div>
            <div class="nav-item" onclick="selectTab(this, 'DIGITAL TWIN')">🎲 DIGITAL TWIN</div>
            <div class="nav-item" onclick="selectTab(this, 'REASONING')">🧠 REASONING</div>
            <div class="nav-item" onclick="selectTab(this, 'SIMULATION')">▶ SIMULATION</div>
            <div class="nav-item" onclick="selectTab(this, 'DECISION')">🛡 DECISION</div>
            <div class="nav-item" onclick="selectTab(this, 'ROBOT CONTROL')">🦾 ROBOT CONTROL</div>
            <div class="nav-item" onclick="selectTab(this, 'FEEDBACK')">🔄 FEEDBACK</div>
            <div class="nav-item" onclick="selectTab(this, 'LEARNING')">📈 LEARNING</div>
            <div class="nav-item" onclick="selectTab(this, 'CALIBRATION')">🎯 CALIBRATION</div>
            <div class="nav-item" onclick="selectTab(this, 'SETTINGS')">⚙ SETTINGS</div>
        </nav>
        
        <!-- Center Core Orb Panel -->
        <div class="center-core">
            <div class="orb-ring"></div>
            <div class="orb-center">
                <div class="orb-title">PHYGENT</div>
                <div class="orb-sub">HYBRID INTELLIGENCE CORE</div>
            </div>
            <div class="node-tag node-real">📷 REAL WORLD<br><small style="color:var(--neon-green)">SENSING...</small></div>
            <div class="node-tag node-twin">🎲 DIGITAL TWIN<br><small style="color:var(--border-cyan)">SYNCHRONIZED</small></div>
            <div class="node-tag node-ai">🧠 AI REASONING<br><small style="color:var(--neon-orange)">THINKING...</small></div>
            <div class="node-tag node-robot">🦾 ROBOT<br><small style="color:var(--neon-green)">EXECUTING...</small></div>
            <div class="node-tag node-learn">📈 LEARNING<br><small style="color:var(--border-cyan)">IMPROVING...</small></div>
            <div class="node-tag node-safe">🛡 SAFETY<br><small style="color:var(--neon-green)">MONITORING...</small></div>
            <div style="position: absolute; bottom: 10px; font-size: 11px; letter-spacing: 2px; color: #567;">"BRIDGING THE PHYSICAL AND DIGITAL WORLDS"</div>
        </div>

        <!-- Right 3D Digital Twin -->
        <div class="digital-twin-panel">
            <div class="panel-header">
                <span>3D ROBOTIC ARM - DIGITAL TWIN</span>
                <span style="color: var(--neon-green); font-size: 11px;">● LIVE SYNC</span>
            </div>
            <div id="canvas3d"></div>
            <div class="xyz-hud">
                <div>X: <b id="val-x">135.0</b> mm</div>
                <div>Y: <b id="val-y">6.0</b> mm</div>
                <div>Z: <b id="val-z">150.0</b> mm</div>
            </div>
            <div class="joints-hud">
                <div>J1: <b id="j1">90°</b></div>
                <div>J2: <b id="j2">45°</b></div>
                <div>J3: <b id="j3">45°</b></div>
                <div>J4: <b id="j4">30°</b></div>
                <div>J5: <b id="j5">10°</b></div>
                <div>Gripper: <b id="grip" style="color:var(--neon-green)">OPEN</b></div>
            </div>
        </div>

        <!-- LLM Panels -->
        <div class="llm-container">
            <div class="llm-card">
                <div class="card-hdr grok-hdr">
                    <span>𝕏 GROK REASONING ENGINE</span>
                    <span style="color:var(--neon-green); font-size:10px;">● LIVE</span>
                </div>
                <div class="card-body" id="grok-text">
                    The detected object is moving towards the right with a speed of 170 px/s. Based on trajectory prediction and current arm position, a direct intercept is the most efficient action. Safety constraints are satisfied.
                </div>
            </div>

            <div class="llm-card">
                <div class="card-hdr nvidia-hdr">
                    <span>🟢 NVIDIA BUILD LLM AUDIT</span>
                    <span style="color:var(--neon-green); font-size:10px;">● LIVE</span>
                </div>
                <div class="card-body" id="nvidia-text">
                    The system performance is within expected range. Error rate: 3.8 px. The latest experience has been stored for continual learning. No anomalies detected. Recommendation: Continue current strategy.
                </div>
            </div>
        </div>

        <!-- Bottom Right Grid -->
        <div class="bottom-right-grid">
            <div class="mini-card">
                <b style="color:var(--border-cyan)">📷 CAMERA VIEW (LIVE)</b>
                <div class="cam-feed">
                    <img src="/video_feed" style="width:100%; height:100%; object-fit:cover;" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                    <div class="cam-ball" style="display:none;"></div>
                </div>
                <div>Person: <b id="cam-person" style="color:var(--neon-green)">Detected</b></div>
                <div>Speed: <b id="cam-speed">170 px/s</b></div>
            </div>


            <div class="mini-card">
                <b style="color:var(--border-cyan)">📈 TRAJECTORY PREDICTION</b>
                <svg width="100%" height="80" style="margin-top:5px;">
                    <path d="M 10 70 Q 60 10 110 50" fill="none" stroke="#00E5FF" stroke-width="2" stroke-dasharray="4"/>
                    <circle cx="110" cy="50" r="6" fill="#FF6600"/>
                </svg>
            </div>

            <div class="mini-card">
                <b style="color:var(--border-cyan)">SYSTEM STATUS</b>
                <div style="font-size:10px; margin-top:5px; line-height:1.6">
                    <div>● Camera: <b style="color:var(--neon-green)">Active</b></div>
                    <div>● ESP32: <b style="color:var(--neon-green)">Connected</b></div>
                    <div>● Twin: <b style="color:var(--neon-green)">Sync</b></div>
                    <div>● Grok: <b style="color:var(--neon-green)">Online</b></div>
                    <div>● NVIDIA: <b style="color:var(--neon-green)">Online</b></div>
                </div>
            </div>
        </div>

        <!-- Voice HUD -->
        <div class="voice-hud">
            <div class="mic-btn" onclick="toggleMic()" style="cursor:pointer">🎙</div>
            <div style="font-size:13px; font-weight:700">VOICE ACTIVE <span style="color:#789; font-weight:400">— Click mic or say "Hey Pygent"</span></div>
            <div style="color:var(--border-cyan); font-style:italic; margin-left:auto" id="voice-msg">"Click mic to speak..."</div>
        </div>


        <!-- Controls -->
        <div class="system-controls">
            <button class="btn-ctrl btn-stop" onclick="triggerControl('STOP')">🛑 STOP</button>
            <button class="btn-ctrl" id="btn-pause" onclick="triggerControl('PAUSE')">⏸ PAUSE</button>
            <button class="btn-ctrl" style="border-color:var(--neon-green)" onclick="triggerControl('HOME')">🏠 HOME</button>
        </div>
    </div>

    <!-- 3D Arm Renderer with Three.js -->
    <script>
        const container = document.getElementById('canvas3d');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x060c18);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(2, 2, 2.5);
        camera.lookAt(0, 0.4, 0);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        // Lighting
        const light = new THREE.DirectionalLight(0x00E5FF, 1.2);
        light.position.set(5, 10, 7);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040, 1.5));

        // Grid Floor
        const grid = new THREE.GridHelper(4, 20, 0x00E5FF, 0x112244);
        scene.add(grid);

        // Full 5-DOF Metallic Robotic Arm Construction in Three.js
        const robotGroup = new THREE.Group();
        
        // Base
        const baseGeo = new THREE.CylinderGeometry(0.35, 0.45, 0.2, 32);
        const baseMat = new THREE.MeshStandardMaterial({ color: 0x111c33, metalness: 0.8, roughness: 0.2 });
        const base = new THREE.Mesh(baseGeo, baseMat);
        base.position.y = 0.1;
        robotGroup.add(base);

        // Joint 1: Base Yaw Group (J1)
        const j1Group = new THREE.Group();
        j1Group.position.y = 0.2;
        robotGroup.add(j1Group);

        const j1HubGeo = new THREE.CylinderGeometry(0.2, 0.2, 0.15, 32);
        const j1HubMat = new THREE.MeshStandardMaterial({ color: 0x00E5FF, metalness: 0.9, roughness: 0.1 });
        const j1Hub = new THREE.Mesh(j1HubGeo, j1HubMat);
        j1Hub.position.y = 0.075;
        j1Group.add(j1Hub);

        // Link 1 (Shoulder)
        const l1Geo = new THREE.BoxGeometry(0.12, 0.5, 0.12);
        const l1Mat = new THREE.MeshStandardMaterial({ color: 0xE0E6ED, metalness: 0.5, roughness: 0.3 });
        const l1 = new THREE.Mesh(l1Geo, l1Mat);
        l1.position.y = 0.325;
        j1Group.add(l1);

        // Joint 2: Shoulder Pitch Group (J2)
        const j2Group = new THREE.Group();
        j2Group.position.y = 0.55;
        j1Group.add(j2Group);

        const j2JointGeo = new THREE.CylinderGeometry(0.1, 0.1, 0.18, 32);
        j2JointGeo.rotateX(Math.PI / 2);
        const j2JointMat = new THREE.MeshStandardMaterial({ color: 0x00E5FF, metalness: 0.9, roughness: 0.1 });
        const j2Joint = new THREE.Mesh(j2JointGeo, j2JointMat);
        j2Group.add(j2Joint);

        // Link 2 (Upper Arm)
        const l2Geo = new THREE.BoxGeometry(0.1, 0.45, 0.1);
        const l2Mat = new THREE.MeshStandardMaterial({ color: 0xE0E6ED, metalness: 0.5, roughness: 0.3 });
        const l2 = new THREE.Mesh(l2Geo, l2Mat);
        l2.position.y = 0.225;
        j2Group.add(l2);

        // Joint 3: Elbow Pitch Group (J3)
        const j3Group = new THREE.Group();
        j3Group.position.y = 0.45;
        j2Group.add(j3Group);

        const j3JointGeo = new THREE.CylinderGeometry(0.08, 0.08, 0.15, 32);
        j3JointGeo.rotateX(Math.PI / 2);
        const j3JointMat = new THREE.MeshStandardMaterial({ color: 0x00FF66, metalness: 0.9, roughness: 0.1 });
        const j3Joint = new THREE.Mesh(j3JointGeo, j3JointMat);
        j3Group.add(j3Joint);

        // Link 3 (Forearm)
        const l3Geo = new THREE.BoxGeometry(0.08, 0.35, 0.08);
        const l3Mat = new THREE.MeshStandardMaterial({ color: 0xE0E6ED, metalness: 0.5, roughness: 0.3 });
        const l3 = new THREE.Mesh(l3Geo, l3Mat);
        l3.position.y = 0.175;
        j3Group.add(l3);

        // Joint 4 & 5: Wrist & Gripper Group (J4 & J5)
        const j4Group = new THREE.Group();
        j4Group.position.y = 0.35;
        j3Group.add(j4Group);

        // Gripper Base
        const gripBaseGeo = new THREE.BoxGeometry(0.12, 0.06, 0.08);
        const gripBaseMat = new THREE.MeshStandardMaterial({ color: 0x111c33 });
        const gripBase = new THREE.Mesh(gripBaseGeo, gripBaseMat);
        gripBase.position.y = 0.03;
        j4Group.add(gripBase);

        // Left & Right Gripper Fingers
        const fingerGeo = new THREE.BoxGeometry(0.02, 0.1, 0.04);
        const fingerMat = new THREE.MeshStandardMaterial({ color: 0x00E5FF });
        
        const fingerL = new THREE.Mesh(fingerGeo, fingerMat);
        fingerL.position.set(-0.04, 0.08, 0);
        j4Group.add(fingerL);

        const fingerR = new THREE.Mesh(fingerGeo, fingerMat);
        fingerR.position.set(0.04, 0.08, 0);
        j4Group.add(fingerR);

        scene.add(robotGroup);

        // Smooth Camera Controls
        let isDragging = false;
        let previousMousePosition = { x: 0, y: 0 };

        container.addEventListener('mousedown', () => isDragging = true);
        container.addEventListener('mouseup', () => isDragging = false);
        container.addEventListener('mousemove', (e) => {
            if (isDragging) {
                const deltaMove = { x: e.offsetX - previousMousePosition.x, y: e.offsetY - previousMousePosition.y };
                robotGroup.rotation.y += deltaMove.x * 0.01;
            }
            previousMousePosition = { x: e.offsetX, y: e.offsetY };
        });


        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();

        // Voice Recognition & Browser Speech Synthesis Core
        let recognition = null;
        let isListening = false;

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                isListening = true;
                document.getElementById('voice-msg').innerText = '"Listening..."';
            };

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('voice-msg').innerText = '"' + transcript + '"';
                
                // Send voice transcript to Python Grok conversational brain
                fetch('/api/voice_command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ transcript: transcript })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.speech_response) {
                        speakText(data.speech_response);
                        document.getElementById('voice-msg').innerText = '"' + data.speech_response + '"';
                    }
                });
            };

            recognition.onend = () => {
                isListening = false;
            };
        }

        function toggleMic() {
            if (!recognition) {
                alert("Speech recognition not supported in this browser.");
                return;
            }
            if (isListening) {
                recognition.stop();
            } else {
                recognition.start();
            }
        }

        let cachedFemaleVoice = null;
        function loadFemaleVoice() {
            if (!('speechSynthesis' in window)) return;
            const voices = window.speechSynthesis.getVoices();
            if (!voices || voices.length === 0) return;

            cachedFemaleVoice = voices.find(v => {
                const name = v.name.toLowerCase();
                return name.includes("zira") || name.includes("female") || name.includes("hazel") || 
                       name.includes("samantha") || name.includes("google us english") || 
                       name.includes("catherine") || name.includes("victoria") || 
                       name.includes("jenny") || name.includes("eva") || name.includes("aria");
            });
        }

        if ('speechSynthesis' in window) {
            window.speechSynthesis.onvoiceschanged = loadFemaleVoice;
            loadFemaleVoice();
        }

        function speakText(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel(); // Stop prior speech
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.95; // Friendly natural cadence
                utterance.pitch = 1.25; // Warm female pitch
                
                if (!cachedFemaleVoice) loadFemaleVoice();
                if (cachedFemaleVoice) {
                    utterance.voice = cachedFemaleVoice;
                }
                window.speechSynthesis.speak(utterance);
            }
        }

        function triggerControl(action) {
            fetch('/api/system_control', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: action })
            })
            .then(res => res.json())
            .then(data => {
                if (data.speech_response) {
                    speakText(data.speech_response);
                    document.getElementById('voice-msg').innerText = '"' + data.speech_response + '"';
                }
            });
        }

        function selectTab(elem, name) {
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            elem.classList.add('active');
            const msg = name + " panel selected!";
            document.getElementById('voice-msg').innerText = '"' + msg + '"';
        }

        // Real-Time Sync Loop
        setInterval(() => {
            fetch('/api/data')
                .then(res => res.json())
                .then(data => {
                    if (data.robot_pos) {
                        document.getElementById('val-x').innerText = data.robot_pos[0].toFixed(1);
                        document.getElementById('val-y').innerText = data.robot_pos[1].toFixed(1);
                        document.getElementById('val-z').innerText = data.robot_pos[2].toFixed(1);
                    }
                    if (data.joints) {
                        document.getElementById('j1').innerText = data.joints[0].toFixed(0) + '°';
                        document.getElementById('j2').innerText = data.joints[1].toFixed(0) + '°';
                        document.getElementById('j3').innerText = data.joints[2].toFixed(0) + '°';
                        document.getElementById('j4').innerText = data.joints[3].toFixed(0) + '°';
                        document.getElementById('j5').innerText = data.joints[4].toFixed(0) + '°';

                        j1Group.rotation.y = (data.joints[0] - 90) * Math.PI / 180;
                        j2Group.rotation.z = (data.joints[1] - 45) * Math.PI / 180;
                        j3Group.rotation.z = (data.joints[2] - 45) * Math.PI / 180;
                        j4Group.rotation.z = (data.joints[3] - 30) * Math.PI / 180;

                    }
                    if (data.grok_reasoning) document.getElementById('grok-text').innerText = data.grok_reasoning;
                    if (data.nvidia_reasoning) document.getElementById('nvidia-text').innerText = data.nvidia_reasoning;
                    if (data.person_present !== undefined) {
                        const pElem = document.getElementById('cam-person');
                        if (pElem) {
                            pElem.innerText = data.person_present ? "Detected 👤" : "Searching...";
                            pElem.style.color = data.person_present ? "var(--neon-green)" : "#89A";
                        }
                    }
                    if (data.speed !== undefined) {
                        const sElem = document.getElementById('cam-speed');
                        if (sElem) sElem.innerText = data.speed.toFixed(0) + " px/s";
                    }
                });
        }, 300);
    </script>
</body>
</html>


"""

if __name__ == "__main__":
    ui = PHYGENTWebUI()
    ui.start()
    time.sleep(2)
