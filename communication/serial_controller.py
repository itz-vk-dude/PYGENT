import serial
import threading
import time
import queue
from typing import Optional, List, Tuple
import config
from communication.protocol import (
    format_move_joints, format_grip, format_home, format_stop,
    format_pause, format_resume, parse_response
)

class SerialController:
    """
    Non-blocking Background Thread ESP32 Serial Communicator.
    Manages physical hardware connection, joint movement commands, real-time telemetry updates,
    and system-wide STOP / PAUSE handling.
    """
    def __init__(self, port: str = None, baudrate: int = None):
        self.port = port or config.DEFAULT_SERIAL_PORT
        self.baudrate = baudrate or config.DEFAULT_SERIAL_BAUD
        self.serial_conn: Optional[serial.Serial] = None
        self.is_running = False
        self._read_thread = None
        
        self.current_joints = [90.0, 45.0, 45.0, 30.0, 90.0]
        self.gripper_state = "OPEN"
        self.status = "DISCONNECTED"
        self.response_queue = queue.Queue()

    def connect(self) -> bool:
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=0.1
            )
            time.sleep(2)  # Wait for ESP32 reset after serial connection
            self.is_running = True
            self.status = "READY"
            
            self._read_thread = threading.Thread(target=self._read_loop, daemon=True)
            self._read_thread.start()
            print(f"[SerialController] Connected to ESP32 on {self.port} at {self.baudrate} baud.")
            return True
        except Exception as e:
            print(f"[SerialController] Connection failed on {self.port}: {e}")
            self.status = "DISCONNECTED"
            self.is_running = False
            return False

    def disconnect(self):
        self.is_running = False
        self.status = "DISCONNECTED"
        if self._read_thread:
            self._read_thread.join(timeout=1.0)
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("[SerialController] Serial connection closed.")

    def _read_loop(self):
        while self.is_running and self.serial_conn and self.serial_conn.is_open:
            try:
                if self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        cmd, args = parse_response(line)
                        if cmd == "JOINTS" and len(args) >= 5:
                            try:
                                self.current_joints = [float(val) for val in args[:5]]
                            except ValueError:
                                pass
                        if cmd:
                            self.response_queue.put((cmd, args))
            except Exception as e:
                time.sleep(0.1)

    def _send_raw(self, msg: str):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(msg.encode('utf-8'))
                self.serial_conn.flush()
            except Exception as e:
                print(f"[SerialController] Send error: {e}")
        else:
            pass  # Simulation fallback mode

    def move_joints(self, j1: float, j2: float, j3: float, j4: float, j5: float):
        msg = format_move_joints(j1, j2, j3, j4, j5)
        self.current_joints = [j1, j2, j3, j4, j5]
        self._send_raw(msg)

    def set_grip(self, state: str):
        self.gripper_state = state
        msg = format_grip(state)
        self._send_raw(msg)

    def home(self):
        self.move_joints(90.0, 45.0, 45.0, 30.0, 90.0)
        msg = format_home()
        self._send_raw(msg)

    def stop(self):
        """REAL HARDWARE STOP FUNCTION"""
        self.status = "STOPPED"
        msg = format_stop()
        self._send_raw(msg)
        print("[SerialController] REAL SYSTEM STOP SIGNAL EXECUTED.")

    def pause(self):
        """REAL HARDWARE PAUSE FUNCTION"""
        self.status = "PAUSED"
        msg = format_pause()
        self._send_raw(msg)
        print("[SerialController] REAL SYSTEM PAUSE SIGNAL EXECUTED.")

    def resume(self):
        """RESUME SYSTEM MOTION"""
        self.status = "READY"
        msg = format_resume()
        self._send_raw(msg)
        print("[SerialController] SYSTEM RESUMED.")
