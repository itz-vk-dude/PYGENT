from communication.esp32_serial import ESP32Controller
from action.command_generator import CommandGenerator
from typing import Dict, Any

class ActionExecutor:
    def __init__(self, esp32_controller: ESP32Controller):
        self.esp32 = esp32_controller
        self.generator = CommandGenerator()

    def execute_action(self, action: Dict[str, Any]) -> bool:
        if not action:
            return False
        
        self.esp32.move_to(action["x"], action["y"], action["z"])
        return True
