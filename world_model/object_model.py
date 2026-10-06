from typing import List, Dict, Any

class ObjectModel:
    """
    Tracked Object Digital Twin Model.
    """
    def __init__(self, name: str = "Tracked Object"):
        self.name = name
        self.position: List[float] = [0.0, 0.0, 0.0]
        self.velocity: List[float] = [0.0, 0.0, 0.0]
        self.radius: float = 15.0

    def update_state(self, position: List[float], velocity: List[float], radius: float = 15.0):
        if len(position) >= 2:
            self.position = [float(position[0]), float(position[1]), float(position[2]) if len(position) > 2 else 0.0]
        if len(velocity) >= 2:
            self.velocity = [float(velocity[0]), float(velocity[1]), float(velocity[2]) if len(velocity) > 2 else 0.0]
        self.radius = float(radius)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "position": list(self.position),
            "velocity": list(self.velocity),
            "radius": self.radius
        }
