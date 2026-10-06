from typing import Dict, Any, List
from robotics.command_generator import CommandGenerator

class ActionExecutor:
    """
    Executes approved physical actions via serial controller or simulation sync.
    """
    def __init__(self):
        self.cmd_gen = CommandGenerator()

    def execute_action(self, action: Dict[str, Any], serial_controller, state_manager):
        if not action or "target_joints" not in action:
            return False, "No target joints specified"

        target_joints = action["target_joints"]
        state_manager.set_commanded_joints(target_joints)

        if serial_controller and serial_controller.is_running:
            serial_controller.move_joints(*target_joints)
            return True, "Command dispatched to physical hardware over serial"
        else:
            # Simulation execution sync
            state_manager.sync_telemetry(target_joints, hardware_connected=False)
            return True, "Executed in SIMULATION mode"
