from typing import List, Tuple, Optional

try:
    import pybullet as p
    import pybullet_data
    PYBULLET_AVAILABLE = True
except ImportError:
    PYBULLET_AVAILABLE = False
    p = None


class PyBulletVisualizer:
    """
    3D Digital Twin Visualizer powered by PyBullet.
    Renders 5-DOF robotic arm, workspace environment, trajectory prediction path, and target ball.
    """
    def __init__(self, gui_mode: bool = True):
        self.gui_mode = gui_mode and PYBULLET_AVAILABLE
        self.physics_client = None
        if PYBULLET_AVAILABLE:
            try:
                self.physics_client = p.connect(p.GUI if self.gui_mode else p.DIRECT)
                p.setAdditionalSearchPath(pybullet_data.getDataPath())
                p.setGravity(0, 0, -9.81)

                p.resetDebugVisualizerCamera(
                    cameraDistance=1.2,
                    cameraYaw=45,
                    cameraPitch=-30,
                    cameraTargetPosition=[0.2, 0.2, 0.2]
                )

                self.plane_id = p.loadURDF("plane.urdf")
                self.arm_id = self._create_5dof_robot_arm()
                self.ball_id = self._create_target_ball()
            except Exception as e:
                print(f"[PyBullet Visualizer] Window init warning: {e}")
                self.gui_mode = False
        else:
            print("[PyBullet Visualizer] PyBullet package not compiled/installed; using visual state sync.")

        self.num_joints = p.getNumJoints(self.arm_id) if PYBULLET_AVAILABLE and self.arm_id else 5

    def _create_5dof_robot_arm(self) -> int:
        """
        Dynamically constructs a 5-DOF Robotic Arm with base, links, revolute joints, and gripper.
        """
        if not PYBULLET_AVAILABLE:
            return 0
        base_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.08, length=0.1, rgbaColor=[0.2, 0.2, 0.25, 1])
        base_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.08, height=0.1)

        link_visuals = [
            p.createVisualShape(p.GEOM_BOX, halfExtents=[0.03, 0.03, 0.06], rgbaColor=[0.1, 0.5, 0.8, 1]),   # J1 Base Yaw
            p.createVisualShape(p.GEOM_BOX, halfExtents=[0.025, 0.025, 0.07], rgbaColor=[0.2, 0.7, 0.3, 1]),  # J2 Shoulder Pitch
            p.createVisualShape(p.GEOM_BOX, halfExtents=[0.02, 0.02, 0.06], rgbaColor=[0.9, 0.6, 0.1, 1]),    # J3 Elbow Pitch
            p.createVisualShape(p.GEOM_BOX, halfExtents=[0.015, 0.015, 0.04], rgbaColor=[0.8, 0.2, 0.2, 1]),  # J4 Wrist Pitch
            p.createVisualShape(p.GEOM_BOX, halfExtents=[0.01, 0.025, 0.02], rgbaColor=[0.9, 0.9, 0.9, 1])    # J5 Gripper
        ]

        link_collisions = [
            p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.03, 0.03, 0.06]),
            p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.025, 0.025, 0.07]),
            p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.02, 0.02, 0.06]),
            p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.015, 0.015, 0.04]),
            p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.01, 0.025, 0.02])
        ]

        masses = [0.5, 0.4, 0.3, 0.2, 0.1]
        link_positions = [[0, 0, 0.08], [0, 0, 0.12], [0, 0, 0.11], [0, 0, 0.08], [0, 0, 0.05]]
        link_orientations = [[0, 0, 0, 1]] * 5
        parent_indices = [0, 1, 2, 3, 4]
        joint_types = [p.JOINT_REVOLUTE] * 5
        joint_axes = [[0, 0, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0]]

        arm_id = p.createMultiBody(
            baseMass=2.0,
            baseCollisionShapeIndex=base_collision,
            baseVisualShapeIndex=base_visual,
            basePosition=[0, 0, 0.05],
            linkMasses=masses,
            linkCollisionShapeIndices=link_collisions,
            linkVisualShapeIndices=link_visuals,
            linkPositions=link_positions,
            linkOrientations=link_orientations,
            linkInertialFramePositions=[[0, 0, 0]] * 5,
            linkInertialFrameOrientations=[[0, 0, 0, 1]] * 5,
            linkParentIndices=parent_indices,
            linkJointTypes=joint_types,
            linkJointAxis=joint_axes
        )

        return arm_id

    def _create_target_ball(self) -> int:
        """Creates a vibrant sphere representing the target ball / predicted path."""
        if not PYBULLET_AVAILABLE:
            return 0
        visual_shape = p.createVisualShape(p.GEOM_SPHERE, radius=0.04, rgbaColor=[1.0, 0.3, 0.1, 0.9])
        collision_shape = p.createCollisionShape(p.GEOM_SPHERE, radius=0.04)
        return p.createMultiBody(baseMass=0.1, baseCollisionShapeIndex=collision_shape, baseVisualShapeIndex=visual_shape, basePosition=[0.3, 0.2, 0.25])

    def update_joints(self, joints_deg: List[float]):
        """
        Updates 3D twin joint positions directly from real hardware servo telemetry angles [J1..J5].
        """
        if not PYBULLET_AVAILABLE or len(joints_deg) < 5:
            return

        import math
        for idx, angle_deg in enumerate(joints_deg[:5]):
            angle_rad = math.radians(angle_deg - 90.0 if idx > 0 else angle_deg)
            p.resetJointState(self.arm_id, idx, angle_rad)

    def update_target_position(self, x_mm: float, y_mm: float, z_mm: float):
        """
        Updates the position of the target ball in PyBullet space (converting mm to meters).
        """
        if not PYBULLET_AVAILABLE:
            return
        x_m, y_m, z_m = x_mm / 1000.0, y_mm / 1000.0, z_mm / 1000.0
        p.resetBasePositionAndOrientation(self.ball_id, [x_m, y_m, z_m], [0, 0, 0, 1])

    def step(self):
        """Steps physics simulation non-blocking."""
        if PYBULLET_AVAILABLE:
            p.stepSimulation()

    def disconnect(self):
        """Cleanly closes PyBullet connection."""
        if PYBULLET_AVAILABLE and p.isConnected():
            p.disconnect()

