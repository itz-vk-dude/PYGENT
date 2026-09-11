import os
from typing import Dict, Any

class PHYGENTDashboard:
    def display(self, data: Dict[str, Any]):
        """
        Renders live pipeline dashboard summarizing perception, prediction, digital twin,
        decision scoring, safety, Grok reasoning, ESP32 status, and continual learning metrics.
        """
        print("\n+------------------------------------------------------------+")
        print("|                      PHYGENT SYSTEM                        |")
        print("+------------------------------------------------------------+")
        print(f"| PERCEPTION: Object={data.get('detected', False)} | Pos=({data.get('x', 0):.1f}, {data.get('y', 0):.1f})")
        print(f"|             Velocity=({data.get('vx', 0):.1f}, {data.get('vy', 0):.1f}) | Speed={data.get('speed', 0):.1f}")
        print("+------------------------------------------------------------+")
        print(f"| DATA QUALITY: Status={data.get('quality_status', 'NORMAL')} | Reason={data.get('quality_reason', 'valid')}")
        print("+------------------------------------------------------------+")
        print(f"| DIGITAL TWIN: Robot Pos={data.get('robot_pos', [0,0,0])} | Gripper={data.get('gripper', 'OPEN')}")
        print("+------------------------------------------------------------+")
        print(f"| HYBRID PREDICTION: ML=({data.get('ml_pred', (0,0))[0]:.1f}, {data.get('ml_pred', (0,0))[1]:.1f})")
        print(f"|                    Physics=({data.get('phys_pred', (0,0))[0]:.1f}, {data.get('phys_pred', (0,0))[1]:.1f})")
        print(f"|                    Hybrid=({data.get('hybrid_pred', (0,0))[0]:.1f}, {data.get('hybrid_pred', (0,0))[1]:.1f})")
        print("+------------------------------------------------------------+")
        print(f"| DECISION & SAFETY: Action={data.get('action_name', 'N/A')} | Target={data.get('action_xyz', (0,0,0))}")
        print(f"|                    Safety={data.get('safety', 'APPROVED')} | Score={data.get('score', 0.0):.2f}")
        print("+------------------------------------------------------------+")
        reasoning_text = str(data.get('grok_reasoning', 'Initializing...'))
        print(f"| GROK REASONING: {reasoning_text[:50]}...")
        print("+------------------------------------------------------------+")
        print(f"| ESP32 STATUS: Connected={data.get('esp32_connected', False)}")
        print("+------------------------------------------------------------+")
        print(f"| FEEDBACK & LEARNING: Error={data.get('error_px', 0.0):.1f} px | Eval={data.get('eval_status', 'SUCCESS')}")
        print(f"|                      Experiences={data.get('experiences', 0)}")
        print("+------------------------------------------------------------+\n")

