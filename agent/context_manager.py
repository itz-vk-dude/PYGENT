from typing import Dict, Any

class ContextManager:
    """
    Assembles compact reasoning context for the agent brain.
    Combines world state, recent events, current task, conversation history, user preferences, safety state.
    """
    def build_context(self, state_manager, user_profile) -> Dict[str, Any]:
        full_st = state_manager.get_state()
        return {
            "system_mode": full_st.get("system_mode", "SIMULATION"),
            "person_present": full_st.get("person_present", False),
            "objects": full_st.get("objects", []),
            "robot_position": full_st.get("robot", {}).get("position", [135, 0, 150]),
            "robot_joints": full_st.get("robot", {}).get("joints_measured", [90, 45, 45, 30, 90]),
            "current_task": full_st.get("task", {}).get("name", "IDLE"),
            "safety_status": full_st.get("safety", {}).get("status", "SAFE"),
            "user_preferences": user_profile.get_preferences(),
            "autonomy_state": full_st.get("agent", {}).get("autonomy_state", "OBSERVE")
        }
