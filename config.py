import os
from pathlib import Path

# Base Directory of the Project
BASE_DIR = Path(__file__).resolve().parent

# Environment Settings
ENV_FILE = BASE_DIR / ".env"

# Hardware & Operational Mode Settings
DEFAULT_SYSTEM_MODE = "SIMULATION"  # "SIMULATION" or "REAL_HARDWARE"
DEFAULT_SERIAL_PORT = "COM3"
DEFAULT_SERIAL_BAUD = 115200

# Camera Settings
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# 5-DOF Robotic Arm Physical Geometry (in mm)
LINK_L1_BASE_HEIGHT = 100.0  # Base to shoulder
LINK_L2_UPPER_ARM = 120.0    # Shoulder to elbow
LINK_L3_FOREARM = 100.0      # Elbow to wrist
LINK_L4_WRIST_EE = 80.0      # Wrist to end-effector

# Joint Servo Angle Limits (Degrees: 0 to 180)
JOINT_LIMITS = {
    "j1": (0.0, 180.0),  # Base Yaw
    "j2": (0.0, 180.0),  # Shoulder Pitch
    "j3": (0.0, 180.0),  # Elbow Pitch
    "j4": (0.0, 180.0),  # Wrist Pitch
    "j5": (0.0, 180.0),  # Wrist Roll / Gripper
}

# Workspace Physical Bounding Box (in mm)
WORKSPACE_BOUNDS = {
    "x_min": -350.0, "x_max": 350.0,
    "y_min": 0.0,    "y_max": 450.0,
    "z_min": 0.0,    "z_max": 350.0
}

# Database Settings
DATABASE_PATH = str(BASE_DIR / "data" / "phygent.db")

# ML Model Paths
ML_MODEL_PATH = str(BASE_DIR / "prediction" / "model.pkl")
CANDIDATE_MODEL_PATH = str(BASE_DIR / "prediction" / "candidate_model.pkl")

# API Keys & LLM Settings
XAI_API_KEY = os.getenv("XAI_API_KEY", "")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
GROK_MODEL_NAME = "grok-beta"
NVIDIA_MODEL_NAME = "nvidia/llama-3.1-nemotron-70b-instruct"

# Audio & Speech Settings
SPEECH_LANGUAGE = "en-US"
ENABLE_TANGLISH_RESPONSE = True

# Autonomy & Decision Thresholds
CONFIDENCE_THRESHOLD = 0.70
SAFETY_MARGIN_MM = 30.0
CONTINUAL_LEARNING_BATCH_SIZE = 10
