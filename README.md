# PHYGENT: Cyber-Physical Proactive AI Agent & Digital Twin System

**PHYGENT** is an adaptive, proactive physical AI agent that operates via a continuous closed loop:
Perception $\rightarrow$ Data Quality $\rightarrow$ Digital Twin / World Model $\rightarrow$ Hybrid Prediction $\rightarrow$ Agent Reasoning $\rightarrow$ What-If Simulation $\rightarrow$ Hard Safety Gate $\rightarrow$ Autonomous Action $\rightarrow$ Observation $\rightarrow$ Feedback $\rightarrow$ Continual Learning.

---

## 🏗️ 17-Package System Architecture

```text
PHYGENT/
├── main.py                   # Master entry point orchestrating agent loop & web app
├── config.py                 # Centralized configuration with relative path resolution
├── requirements.txt          # System dependencies
├── .env                      # API keys (GROK_API_KEY, NVIDIA_API_KEY)
├── README.md                 # System documentation
│
├── agent/                    # Core Agent Orchestrator, Context, Autonomy State Machine, Tasks
├── physical_world/           # Camera Stream, ESP32 Connection, Physical Environment & Robot State
├── perception/               # HSV Detector, Trajectory Tracker, Human & Scene Understanding
├── data/                     # Data Collector, SQLite Audit Database (18 tables), Quality Gate
├── world_model/              # Single Source of Truth PHYGENT_STATE Manager & Telemetry Sync
├── prediction/               # Random Forest ML, Kinematic Physics, Hybrid Predictor & Evaluator
├── reasoning/                # xAI Grok API Integration, Prompts, Tanglish Dialogue Engine
├── simulation/               # Candidate Action Generator, Trajectory & Digital Twin Simulator
├── decision/                 # Action Scorer, Hard-Gate Safety Engine, Autonomy Policy
├── robotics/                 # 5-DOF Arm FK/IK Kinematics, Motion Planner, Serial Executor
├── communication/            # Serial Protocol, ESP32 Controller with Real STOP & PAUSE
├── feedback/                 # Verified Camera/Telemetry Observation, Comparator, Evaluator
├── learning/                 # Dataset Manager, Continual Learning, Model Validation & Rollback
├── interaction/              # Decoupled Speech Input/Output (TTS Queue), Conversation, User Memory
├── calibration/              # Camera-to-Robot Frame Transformation & Workspace Boundaries
├── interface/                # Flask Web App, REST API & SSE Stream, 7-Page HTML Dashboard
└── tests/                    # Unit and Integration Test Suite
```

---

## 🚀 Getting Started

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables (`.env`):**
   ```env
   GROK_API_KEY=your_grok_api_key
   NVIDIA_API_KEY=your_nvidia_api_key
   ```

### Operational Modes

#### 1. Simulation Mode (Default)
Run in virtual simulation mode without physical hardware:
```bash
python main.py --mode SIMULATION --web-port 5000
```
- Dashboard available at `http://localhost:5000`
- Live 3D Digital Twin visualization in Three.js
- Synthetic frame fallback for development testing

#### 2. Real Hardware Mode
Connect to an ESP32 micro-controller and physical camera:
```bash
python main.py --mode REAL_HARDWARE --port COM3 --web-port 5000
```

---

## 🧪 Testing

Run full test suite:
```bash
python -m unittest discover tests
```
