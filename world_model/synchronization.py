from typing import List, Dict, Any

class TelemetrySynchronizer:
    """
    Enforces the distinction: COMMANDED != MEASURED.
    Synchronizes confirmed serial telemetry into the Digital Twin measured state.
    """
    def sync(self, robot_model, measured_joints: List[float], hardware_connected: bool):
        if hardware_connected and len(measured_joints) >= 5:
            robot_model.update_measured_joints(measured_joints)
            robot_model.status = "ONLINE_HARDWARE"
        else:
            robot_model.status = "SIMULATION"
