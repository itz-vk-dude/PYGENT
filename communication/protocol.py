"""
PHYGENT Serial Communication Protocol Definition
Commands:
  MOVE,J1,J2,J3,J4,J5
  GRIP,OPEN or GRIP,CLOSE
  HOME
  STOP
  PAUSE
  RESUME
  STATUS
  POSITION
  JOINTS
Responses:
  READY
  MOVING
  REACHED,X,Y,Z
  JOINTS,J1,J2,J3,J4,J5
  POSITION,X,Y,Z
  ERROR,REASON
"""

CMD_MOVE_JOINTS = "MOVE"
CMD_GRIP = "GRIP"
CMD_HOME = "HOME"
CMD_STOP = "STOP"
CMD_PAUSE = "PAUSE"
CMD_RESUME = "RESUME"
CMD_STATUS = "STATUS"

RESP_READY = "READY"
RESP_MOVING = "MOVING"
RESP_REACHED = "REACHED"
RESP_JOINTS = "JOINTS"
RESP_POSITION = "POSITION"
RESP_ERROR = "ERROR"

def format_move_joints(j1: float, j2: float, j3: float, j4: float, j5: float) -> str:
    return f"{CMD_MOVE_JOINTS},{j1:.1f},{j2:.1f},{j3:.1f},{j4:.1f},{j5:.1f}\n"

def format_grip(state: str) -> str:
    return f"{CMD_GRIP},{state.upper()}\n"

def format_home() -> str:
    return f"{CMD_HOME}\n"

def format_stop() -> str:
    return f"{CMD_STOP}\n"

def format_pause() -> str:
    return f"{CMD_PAUSE}\n"

def format_resume() -> str:
    return f"{CMD_RESUME}\n"

def parse_response(response: str):
    parts = response.strip().split(",")
    if not parts or parts[0] == "":
        return None, []
    return parts[0], parts[1:]
