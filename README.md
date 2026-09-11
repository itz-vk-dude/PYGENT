# PHYGENT: Cyber-Physical AI Agent & Digital Twin Framework

**PHYGENT** is a closed-loop Cyber-Physical Intelligence & Robotics Framework that bridges real-world perception, machine learning, physics-based predictions, digital twin kinematics, LLM reasoning (Grok & NVIDIA), PyBullet simulation, and micro-controller hardware execution (ESP32).

---

## 🌟 Key Features

- **Real-Time Perception Engine**: Computer vision tracking (OpenCV) supporting dynamic object and person detection, speed/direction telemetry, and camera streaming.
- **Digital Twin & Kinematics**: Inverse Kinematic (IK) solvers for robotic arms, state synchronization, and PyBullet visualization.
- **Hybrid Prediction Model**: Combines ML trajectory predictions with analytical physical state forecasting.
- **LLM Reasoning & Audit**: Powered by **xAI Grok** and **NVIDIA NIM API** for voice intent resolution, decision explanation, and closed-loop feedback auditing.
- **Multi-Modal User Interface**:
  - **Live Web UI Dashboard** (Flask / WebSockets / HTML5) with video feed and telemetry graphs.
  - **JARVIS Voice Engine**: Continuous speech command processing for real-time manual arm adjustments and operating state changes (`HOME`, `STOP`, `PAUSE`).
- **Hardware Integration**: Serial communication with ESP32 board (`pyserial`) for real motor state execution and feedback telemetry.
- **Continual Learning & Feedback**: Dynamic observation collection, comparator checks, self-evaluation, and online model updates.

---

## 🏗️ System Architecture

```
                               ┌─────────────────────────┐
                               │     Web UI / Dashboard  │
                               │   JARVIS Voice Interface│
                               └────────────┬────────────┘
                                            │
┌──────────────────┐           ┌────────────▼────────────┐           ┌──────────────────┐
│  Physical Camera │──────────►│    Perception Engine    │──────────►│ Data Quality & DB│
└──────────────────┘           └────────────┬────────────┘           └──────────────────┘
                                            │
                               ┌────────────▼────────────┐
                               │    Digital Twin State   │
                               └────────────┬────────────┘
                                            │
                               ┌────────────▼────────────┐
                               │    Hybrid Predictor     │
                               │   (ML + Physics Engine) │
                               └────────────┬────────────┘
                                            │
                               ┌────────────▼────────────┐
                               │ Candidate Actions &     │
                               │ PyBullet Simulator      │
                               └────────────┬────────────┘
                                            │
                               ┌────────────▼────────────┐
                               │  Decision & IK Solver   │
                               └───────┬───────────┬─────┘
                                       │           │
             ┌─────────────────────────┘           └─────────────────────────┐
             ▼                                                               ▼
┌──────────────────────────┐                                   ┌──────────────────────────┐
│ ESP32 Hardware Executor  │                                   │   LLM Reasoning Core     │
│  (Robotic Arm Servos)    │                                   │  (Grok / NVIDIA NIM API) │
└──────────────────────────┘                                   └──────────────────────────┘
```

---

## 📁 Repository Structure

```
PYGENT/
├── action/              # Action execution handlers
├── calibration/         # Camera and sensor calibration routines
├── camera/              # Camera input interfaces
├── communication/       # ESP32 serial communication & motor control
├── data/                # Data quality monitoring and sqlite database operations
├── decision/            # Decision engine & risk evaluation
├── digital_twin/        # Robotic kinematics (IK/FK), state manager, PyBullet renderer
├── feedback/            # Closed-loop feedback comparator & self-evaluation
├── interface/           # Web UI dashboard, JARVIS GUI & Voice Engine
├── learning/            # Continual online learning module
├── llm/                 # LLM wrappers & system prompts
├── ml/                  # Machine learning training scripts
├── perception/          # OpenCV visual object tracking & feature extraction
├── physical_world/      # Hardware physical stream abstraction
├── prediction/          # Physics + ML hybrid predictor
├── reasoning/           # Grok API & NVIDIA API reasoning integration
├── simulation/          # Candidate action generator & physics simulation
├── config.py            # Global system configurations
├── main.py              # Main execution loop
└── requirements.txt     # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Webcam / Camera Device
- (Optional) ESP32 micro-controller flashed with serial motor listener script
- (Optional) NVIDIA API / Grok API keys set in `.env`

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/itz-vk-dude/PYGENT.git
   cd PYGENT
   ```

2. **Create a Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Configure Environment Variables (Optional):**
   Create a `.env` file in the root directory:
   ```env
   GROK_API_KEY=your_grok_api_key
   NVIDIA_API_KEY=your_nvidia_api_key
   ```

---

## ⚙️ Running PHYGENT

### Simulation Mode (Default)
Run the full loop in virtual simulation mode without hardware attached:
```bash
python main.py
```
This launches:
- Web Dashboard on `http://localhost:5000`
- Synthetic/Webcam perception tracking
- Inverse Kinematics calculations & digital twin updates
- LLM decision audits

### Hardware Execution Mode
To connect to an active ESP32 device on a serial port (e.g. `COM3` or `/dev/ttyUSB0`):
```python
from main import run_phygent_loop

run_phygent_loop(serial_port="COM3", simulation_mode=False)
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
