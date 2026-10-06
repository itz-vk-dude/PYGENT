from typing import Dict, Any, List

class TelemetryReceiver:
    """
    Parses incoming telemetry from serial hardware queue and updates Digital Twin state.
    """
    def process_telemetry(self, serial_controller, state_manager):
        if not serial_controller or not serial_controller.is_running:
            return

        while not serial_controller.response_queue.empty():
            cmd, args = serial_controller.response_queue.get()
            if cmd == "JOINTS" and len(args) >= 5:
                try:
                    joints = [float(a) for a in args[:5]]
                    state_manager.sync_telemetry(joints, hardware_connected=True, gripper_state=serial_controller.gripper_state)
                except ValueError:
                    pass
