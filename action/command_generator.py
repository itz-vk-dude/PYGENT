from communication.protocol import format_move_to, format_grip, format_home, format_stop
from typing import Dict, Any

class CommandGenerator:
    def create_move_command(self, action: Dict[str, Any]) -> str:
        x, y, z = action.get("x", 0.0), action.get("y", 0.0), action.get("z", 0.0)
        return format_move_to(x, y, z)

    def create_grip_command(self, state: str) -> str:
        return format_grip(state)
