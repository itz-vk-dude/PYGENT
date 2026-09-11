class RobotModel:
    def __init__(self):
        self.joint_angles = [0.0, 0.0, 0.0, 0.0]
        self.gripper_state = "OPEN"
        self.current_position = [0.0, 0.0, 0.0]
        self.workspace_bounds = {
            "x_min": -300.0, "x_max": 300.0,
            "y_min": 0.0,    "y_max": 400.0,
            "z_min": 0.0,    "z_max": 300.0
        }

    def update_joints(self, angles: list):
        self.joint_angles = angles

    def update_gripper(self, state: str):
        self.gripper_state = state

    def update_position(self, pos: list):
        self.current_position = pos
