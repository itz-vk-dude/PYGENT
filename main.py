import time
import threading
import sys
import argparse
import config
from agent.agent_core import PHYGENTAgentCore
from interface.web_app import create_app

def main():
    parser = argparse.ArgumentParser(description="PHYGENT Physical AI Agent System")
    parser.add_argument("--mode", type=str, default="SIMULATION", choices=["SIMULATION", "REAL_HARDWARE"], help="Operational mode")
    parser.add_argument("--port", type=str, default="COM3", help="Serial port for ESP32 hardware")
    parser.add_argument("--web-port", type=int, default=5000, help="Web UI HTTP server port")
    args = parser.parse_args()

    print(f"============================================================")
    print(f"           PHYGENT — PHYSICAL AI AGENT CORE V1              ")
    print(f"============================================================")
    print(f" Operational Mode: [{args.mode}]")
    print(f" Serial Port:      [{args.port}]")
    print(f" Web Dashboard:    [http://localhost:{args.web_port}]")
    print(f"============================================================\n")

    # Initialize Central Agent Core Orchestrator
    agent = PHYGENTAgentCore(serial_port=args.port, system_mode=args.mode)

    # Initialize Flask Web Interface
    app = create_app(state_store=agent.state_manager, agent_core=agent)

    # Start Agent Closed-Loop background thread
    def agent_loop():
        while True:
            try:
                agent.step()
                time.sleep(0.1)
            except Exception as e:
                print(f"[Main Loop Error]: {e}")
                time.sleep(0.5)

    agent_thread = threading.Thread(target=agent_loop, daemon=True)
    agent_thread.start()

    print("[PHYGENT System] Master closed loop active. Running web app...")
    try:
        app.run(host="0.0.0.0", port=args.web_port, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n[PHYGENT System] Shutdown requested by user.")
    finally:
        if args.mode == "REAL_HARDWARE":
            agent.serial_controller.disconnect()
            agent.camera.stop()
        print("[PHYGENT System] Shutdown complete.")

if __name__ == "__main__":
    main()
