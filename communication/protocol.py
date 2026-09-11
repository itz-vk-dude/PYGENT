"""
Serial Communication Protocol Definition

This module defines the commands and expected responses for the 
communication between the Python intelligence layer and the ESP32 hardware layer.

All messages should be newline terminated ('\n').
"""

# Commands sent from Python to ESP32
CMD_MOVE_TO = "MOVE_TO"      # Format: MOVE_TO,X,Y,Z
CMD_MOVE_JOINTS = "MOVE"     # Format: MOVE,J1,J2,J3,J4,J5
CMD_GRIP = "GRIP"            # Format: GRIP,OPEN or GRIP,CLOSE
CMD_HOME = "HOME"            # Format: HOME
CMD_STOP = "STOP"            # Format: STOP

# Responses sent from ESP32 to Python
RESP_READY = "READY"
RESP_MOVING = "MOVING"
RESP_REACHED = "REACHED"     # Format: REACHED,X,Y,Z
RESP_JOINTS = "JOINTS"       # Format: JOINTS,J1,J2,J3,J4,J5
RESP_POSITION = "POSITION"   # Format: POSITION,X,Y,Z
RESP_GRIPPER = "GRIPPER"     # Format: GRIPPER,OPEN/CLOSE
RESP_STATUS = "STATUS"       # Format: STATUS,MOVING/READY
RESP_GRIP_CLOSED = "GRIP_CLOSED"
RESP_GRIP_OPENED = "GRIP_OPENED"
RESP_ERROR = "ERROR"         # Format: ERROR,REASON

def format_move_to(x: float, y: float, z: float) -> str:
    """Formats a MOVE_TO command."""
    return f"{CMD_MOVE_TO},{x:.1f},{y:.1f},{z:.1f}\n"

def format_move_joints(j1: float, j2: float, j3: float, j4: float, j5: float) -> str:
    """Formats a MOVE command using 5-DOF joint angles."""
    return f"{CMD_MOVE_JOINTS},{j1:.1f},{j2:.1f},{j3:.1f},{j4:.1f},{j5:.1f}\n"

def format_grip(state: str) -> str:
    """Formats a GRIP command. state must be 'OPEN' or 'CLOSE'."""
    if state not in ("OPEN", "CLOSE"):
        raise ValueError("Grip state must be 'OPEN' or 'CLOSE'")
    return f"{CMD_GRIP},{state}\n"

def format_home() -> str:
    """Formats a HOME command."""
    return f"{CMD_HOME}\n"

def format_stop() -> str:
    """Formats a STOP command."""
    return f"{CMD_STOP}\n"

def parse_response(response: str):
    """
    Parses a response from the ESP32.
    Returns a tuple of (command, args)
    """
    parts = response.strip().split(",")
    if not parts or parts[0] == "":
        return None, []
    
    cmd = parts[0]
    args = parts[1:]
    return cmd, args
