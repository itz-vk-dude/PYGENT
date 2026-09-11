import serial
import threading
import time
import queue
from typing import Optional, Callable
from communication.protocol import format_move_to, format_grip, format_home, format_stop, parse_response

class ESP32Controller:
    def __init__(self, port: str, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn: Optional[serial.Serial] = None
        
        self.is_running = False
        self._read_thread = None
        self.current_joints = [90.0, 45.0, 45.0, 30.0, 90.0]
        self.gripper_state = "OPEN"

    def connect(self) -> bool:
        """Establishes serial connection with the ESP32."""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=0.1
            )
            time.sleep(2)  # Wait for ESP32 to reset after serial connection
            self.is_running = True
            
            # Start background thread to read from serial non-blocking
            self._read_thread = threading.Thread(target=self._read_loop, daemon=True)
            self._read_thread.start()
            print(f"Connected to ESP32 on {self.port}")
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to ESP32 on {self.port}: {e}")
            return False

    def disconnect(self):
        """Closes the serial connection."""
        self.is_running = False
        if self._read_thread:
            self._read_thread.join(timeout=1.0)
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from ESP32")

    def _read_loop(self):
        """Continuously reads from the serial port in a background thread."""
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
                            # Push to queue
                            self.response_queue.put((cmd, args))
                            # Trigger callback if set
                            if self.on_response_callback:
                                self.on_response_callback(cmd, args)
            except Exception as e:
                print(f"Serial read error: {e}")
                time.sleep(0.1)

    def _send_raw(self, msg: str):
        """Sends a raw string message over serial."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.write(msg.encode('utf-8'))
            self.serial_conn.flush()
        else:
            print(f"Cannot send command, serial not connected: {msg.strip()}")

    # High-level command methods
    
    def move_to(self, x: float, y: float, z: float):
        msg = format_move_to(x, y, z)
        self._send_raw(msg)

    def move_joints(self, j1: float, j2: float, j3: float, j4: float, j5: float):
        from communication.protocol import format_move_joints
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
        msg = format_stop()
        self._send_raw(msg)