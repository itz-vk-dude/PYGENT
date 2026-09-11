import tkinter as tk
from tkinter import ttk
from typing import Dict, Any

class JARVISDashboardGUI:
    """
    Futuristic JARVIS Dark-Themed GUI Dashboard for PHYGENT.
    Displays live perception metrics, ML/Physics predictions, Grok LLM reasoning,
    decision safety scoring, and real-time ESP32 hardware servo telemetry.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PHYGENT — JARVIS HYBRID INTELLIGENCE CORE")
        self.root.geometry("850x600")
        self.root.configure(bg="#0B0F19")

        self.setup_styles()
        self.build_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#0B0F19")
        self.style.configure("Header.TLabel", font=("Consolas", 16, "bold"), foreground="#00E5FF", background="#0B0F19")
        self.style.configure("Section.TLabel", font=("Consolas", 11, "bold"), foreground="#76FF03", background="#121829")
        self.style.configure("Content.TLabel", font=("Consolas", 10), foreground="#E0E6ED", background="#121829")

    def build_widgets(self):
        # Header Bar
        header_frame = tk.Frame(self.root, bg="#121829", highlightbackground="#00E5FF", highlightthickness=1)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        lbl_title = tk.Label(
            header_frame,
            text="P H Y G E N T   |   H Y B R I D   I N T E L L I G E N C E   C O R E",
            font=("Consolas", 14, "bold"),
            fg="#00E5FF",
            bg="#121829",
            pady=8
        )
        lbl_title.pack()

        # Grid Container
        container = tk.Frame(self.root, bg="#0B0F19")
        container.pack(fill="both", expand=True, padx=10, pady=5)

        # Top Left Panel: Perception & Data Quality
        panel_percep = tk.LabelFrame(container, text=" 👁 PERCEPTION & DATA QUALITY ", font=("Consolas", 10, "bold"), fg="#00E5FF", bg="#121829", bd=1, relief="solid")
        panel_percep.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.lbl_object = tk.Label(panel_percep, text="OBJECT DETECTED: FALSE", font=("Consolas", 10, "bold"), fg="#FF5252", bg="#121829")
        self.lbl_object.pack(anchor="w", padx=10, pady=3)

        self.lbl_pos = tk.Label(panel_percep, text="POSITION (X,Y): (0.0, 0.0) px", font=("Consolas", 10), fg="#E0E6ED", bg="#121829")
        self.lbl_pos.pack(anchor="w", padx=10, pady=2)

        self.lbl_vel = tk.Label(panel_percep, text="VELOCITY: (0.0, 0.0) px/s", font=("Consolas", 10), fg="#E0E6ED", bg="#121829")
        self.lbl_vel.pack(anchor="w", padx=10, pady=2)

        self.lbl_quality = tk.Label(panel_percep, text="QUALITY STATUS: NORMAL", font=("Consolas", 10), fg="#76FF03", bg="#121829")
        self.lbl_quality.pack(anchor="w", padx=10, pady=2)

        # Top Right Panel: ESP32 Hardware Telemetry
        panel_hw = tk.LabelFrame(container, text=" 🤖 ESP32 SERVO TELEMETRY & TWIN ", font=("Consolas", 10, "bold"), fg="#00E5FF", bg="#121829", bd=1, relief="solid")
        panel_hw.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.lbl_esp_status = tk.Label(panel_hw, text="ESP32 STATUS: SIMULATION / DRY-RUN", font=("Consolas", 10, "bold"), fg="#FFD700", bg="#121829")
        self.lbl_esp_status.pack(anchor="w", padx=10, pady=3)

        self.lbl_joints = tk.Label(panel_hw, text="JOINTS (J1..J5): 90.0° | 45.0° | 45.0° | 30.0° | 90.0°", font=("Consolas", 10), fg="#E0E6ED", bg="#121829")
        self.lbl_joints.pack(anchor="w", padx=10, pady=2)

        self.lbl_cartesian = tk.Label(panel_hw, text="FK POSITION (X,Y,Z): (135.0, 6.0, 150.0) mm", font=("Consolas", 10), fg="#E0E6ED", bg="#121829")
        self.lbl_cartesian.pack(anchor="w", padx=10, pady=2)

        self.lbl_twin_sync = tk.Label(panel_hw, text="3D TWIN SYNC: ● ACTIVE (PyBullet GUI)", font=("Consolas", 10, "bold"), fg="#76FF03", bg="#121829")
        self.lbl_twin_sync.pack(anchor="w", padx=10, pady=2)

        # Middle Left Panel: Hybrid Prediction Engine
        panel_pred = tk.LabelFrame(container, text=" 🧠 HYBRID PREDICTION ENGINE ", font=("Consolas", 10, "bold"), fg="#00E5FF", bg="#121829", bd=1, relief="solid")
        panel_pred.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.lbl_ml = tk.Label(panel_pred, text="ML MODEL PRED: (0.0, 0.0) px", font=("Consolas", 10), fg="#E0E6ED", bg="#121829")
        self.lbl_ml.pack(anchor="w", padx=10, pady=2)

        self.lbl_phys = tk.Label(panel_pred, text="PHYSICS MODEL PRED: (0.0, 0.0) px", font=("Consolas", 10), fg="#E0E6ED", bg="#121829")
        self.lbl_phys.pack(anchor="w", padx=10, pady=2)

        self.lbl_hybrid = tk.Label(panel_pred, text="HYBRID ENSEMBLE: (0.0, 0.0) px", font=("Consolas", 10, "bold"), fg="#76FF03", bg="#121829")
        self.lbl_hybrid.pack(anchor="w", padx=10, pady=2)

        # Middle Right Panel: Decision & Safety Scoring
        panel_dec = tk.LabelFrame(container, text=" 🛡 DECISION & SAFETY SCORING ", font=("Consolas", 10, "bold"), fg="#00E5FF", bg="#121829", bd=1, relief="solid")
        panel_dec.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.lbl_action = tk.Label(panel_dec, text="ACTION: DIRECT INTERCEPT", font=("Consolas", 10, "bold"), fg="#00E5FF", bg="#121829")
        self.lbl_action.pack(anchor="w", padx=10, pady=2)

        self.lbl_score = tk.Label(panel_dec, text="DECISION SCORE: 0.00", font=("Consolas", 10), fg="#E0E6ED", bg="#121829")
        self.lbl_score.pack(anchor="w", padx=10, pady=2)

        self.lbl_safety = tk.Label(panel_dec, text="SAFETY CHECK: APPROVED", font=("Consolas", 10, "bold"), fg="#76FF03", bg="#121829")
        self.lbl_safety.pack(anchor="w", padx=10, pady=2)

        # Bottom Panel: Dual LLM Core (Grok Interception + NVIDIA Build Audit)
        panel_llm = tk.LabelFrame(container, text=" ⚡ DUAL LLM REASONING & AUDIT CORE ", font=("Consolas", 10, "bold"), fg="#00E5FF", bg="#121829", bd=1, relief="solid")
        panel_llm.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Grok LLM Box
        lbl_grok_hdr = tk.Label(panel_llm, text="[GROK REASONING ENGINE]", font=("Consolas", 9, "bold"), fg="#00E5FF", bg="#121829")
        lbl_grok_hdr.grid(row=0, column=0, sticky="w", padx=8, pady=(4, 0))

        self.txt_grok = tk.Text(panel_llm, height=4, width=45, font=("Consolas", 9), fg="#00E5FF", bg="#0B0F19", wrap="word", bd=1, relief="solid")
        self.txt_grok.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        self.txt_grok.insert("1.0", "Grok API initializing trajectory decision reasoning...")

        # NVIDIA Build LLM Box
        lbl_nvidia_hdr = tk.Label(panel_llm, text="[NVIDIA BUILD LLM AUDIT]", font=("Consolas", 9, "bold"), fg="#76FF03", bg="#121829")
        lbl_nvidia_hdr.grid(row=0, column=1, sticky="w", padx=8, pady=(4, 0))

        self.txt_nvidia = tk.Text(panel_llm, height=4, width=45, font=("Consolas", 9), fg="#76FF03", bg="#0B0F19", wrap="word", bd=1, relief="solid")
        self.txt_nvidia.grid(row=1, column=1, sticky="nsew", padx=8, pady=4)
        self.txt_nvidia.insert("1.0", "NVIDIA AutoGen-15 initializing continual learning feedback audit...")

        panel_llm.columnconfigure(0, weight=1)
        panel_llm.columnconfigure(1, weight=1)
        panel_llm.rowconfigure(1, weight=1)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)
        container.rowconfigure(2, weight=1)

    def update_data(self, data: Dict[str, Any]):
        """Updates GUI widgets with live telemetry and inference data."""
        det = data.get("detected", False)
        self.lbl_object.config(text=f"OBJECT DETECTED: {'TRUE' if det else 'FALSE'}", fg="#76FF03" if det else "#FF5252")
        self.lbl_pos.config(text=f"POSITION (X,Y): ({data.get('x', 0):.1f}, {data.get('y', 0):.1f}) px")
        self.lbl_vel.config(text=f"VELOCITY: ({data.get('vx', 0):.1f}, {data.get('vy', 0):.1f}) px/s")
        self.lbl_quality.config(text=f"QUALITY STATUS: {data.get('quality_status', 'NORMAL')}")

        conn = data.get("esp32_connected", False)
        self.lbl_esp_status.config(text=f"ESP32 STATUS: {'● CONNECTED' if conn else '● SIMULATION MODE'}", fg="#76FF03" if conn else "#FFD700")

        joints = data.get("joints", [90.0, 45.0, 45.0, 30.0, 90.0])
        self.lbl_joints.config(text=f"JOINTS (J1..J5): {joints[0]:.1f}° | {joints[1]:.1f}° | {joints[2]:.1f}° | {joints[3]:.1f}° | {joints[4]:.1f}°")

        robot_pos = data.get("robot_pos", [0, 0, 0])
        self.lbl_cartesian.config(text=f"FK POSITION (X,Y,Z): ({robot_pos[0]:.1f}, {robot_pos[1]:.1f}, {robot_pos[2]:.1f}) mm")

        ml = data.get("ml_pred", (0, 0))
        phys = data.get("phys_pred", (0, 0))
        hyb = data.get("hybrid_pred", (0, 0))
        self.lbl_ml.config(text=f"ML MODEL PRED: ({ml[0]:.1f}, {ml[1]:.1f}) px")
        self.lbl_phys.config(text=f"PHYSICS MODEL PRED: ({phys[0]:.1f}, {phys[1]:.1f}) px")
        self.lbl_hybrid.config(text=f"HYBRID ENSEMBLE: ({hyb[0]:.1f}, {hyb[1]:.1f}) px")

        self.lbl_action.config(text=f"ACTION: {data.get('action_name', 'DIRECT INTERCEPT')}")
        self.lbl_score.config(text=f"DECISION SCORE: {data.get('score', 0.0):.2f}")
        
        saf = data.get("safety", "APPROVED")
        self.lbl_safety.config(text=f"SAFETY CHECK: {saf}", fg="#76FF03" if "APPROVED" in saf else "#FF5252")

        grok_reasoning = str(data.get("grok_reasoning", ""))
        nvidia_reasoning = str(data.get("nvidia_reasoning", ""))
        
        self.txt_grok.delete("1.0", tk.END)
        self.txt_grok.insert("1.0", grok_reasoning)

        self.txt_nvidia.delete("1.0", tk.END)
        self.txt_nvidia.insert("1.0", nvidia_reasoning)

        self.root.update_idletasks()
        self.root.update()


