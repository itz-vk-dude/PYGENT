from typing import List

class CommandGenerator:
    """
    Formats standard string commands for ESP32 serial communication.
    """
    def format_move_joints(self, j1: float, j2: float, j3: float, j4: float, j5: float) -> str:
        return f"MOVE,{j1:.1f},{j2:.1f},{j3:.1f},{j4:.1f},{j5:.1f}\n"

    def format_grip(self, state: str) -> str:
        return f"GRIP,{state.upper()}\n"

    def format_stop(self) -> str:
        return "STOP\n"

    def format_pause(self) -> str:
        return "PAUSE\n"

    def format_resume(self) -> str:
        return "RESUME\n"

    def format_home(self) -> str:
        return "HOME\n"
