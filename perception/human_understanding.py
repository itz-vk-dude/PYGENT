from typing import Dict, Any, List

class HumanUnderstanding:
    """
    Analyzes human presence, position, workspace encroachment, and approach velocity.
    """
    def analyze(self, detection: Dict[str, Any], tracking: Dict[str, Any], workspace_center: List[float] = None) -> Dict[str, Any]:
        if workspace_center is None:
            workspace_center = [320.0, 240.0]

        person_present = detection.get("person_present", False)
        px, py = detection.get("x", 0.0), detection.get("y", 0.0)

        dist_to_workspace = ((px - workspace_center[0])**2 + (py - workspace_center[1])**2)**0.5 if person_present else 999.0
        inside_workspace = person_present and (dist_to_workspace < 150.0)
        
        # Check approaching direction towards workspace center
        vx, vy = tracking.get("vx", 0.0), tracking.get("vy", 0.0)
        approaching = False
        if person_present and (vx != 0 or vy != 0):
            dx = workspace_center[0] - px
            dy = workspace_center[1] - py
            dot_product = dx * vx + dy * vy
            approaching = dot_product > 0

        return {
            "human_present": person_present,
            "human_position": [px, py] if person_present else [],
            "distance_to_workspace": round(dist_to_workspace, 1),
            "inside_workspace": inside_workspace,
            "approaching_workspace": approaching
        }
