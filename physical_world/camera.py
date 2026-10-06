import cv2
import threading
import time
import numpy as np
from typing import Optional
import config

class CameraStream:
    """
    Threaded OpenCV Camera Stream Controller.
    If physical webcam is unavailable, marks status as CAMERA_OFFLINE.
    Synthetic frame generation is available ONLY when explicitly requested for DEVELOPMENT SIMULATION.
    """
    def __init__(self, camera_index: int = None):
        self.camera_index = camera_index if camera_index is not None else config.CAMERA_INDEX
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.frame: Optional[np.ndarray] = None
        self.lock = threading.Lock()
        self.is_online = False
        self.fps = 0.0

    def start(self) -> bool:
        """Starts the video capture thread."""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                print(f"[CameraStream] WARNING: Physical camera index {self.camera_index} could not be opened.")
                self.is_online = False
                return False
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
            self.cap.set(cv2.CAP_PROP_FPS, config.CAMERA_FPS)
            
            self.is_running = True
            self.is_online = True
            self.thread = threading.Thread(target=self._update_loop, daemon=True)
            self.thread.start()
            print(f"[CameraStream] Physical camera index {self.camera_index} online.")
            return True
        except Exception as e:
            print(f"[CameraStream] Camera initialization error: {e}")
            self.is_online = False
            return False

    def _update_loop(self):
        last_time = time.time()
        while self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            now = time.time()
            dt = now - last_time
            last_time = now
            if dt > 0:
                self.fps = 0.9 * self.fps + 0.1 * (1.0 / dt)

            if ret and frame is not None:
                with self.lock:
                    self.frame = frame.copy()
                    self.is_online = True
            else:
                with self.lock:
                    self.is_online = False
                time.sleep(0.01)

    def get_frame(self) -> Optional[np.ndarray]:
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
            return None

    def get_synthetic_dev_frame(self, step: int) -> np.ndarray:
        """
        STRICTLY FOR DEVELOPMENT SIMULATION TESTING ONLY.
        Generates a synthetic frame with a moving circle to test visual detection without a physical camera.
        """
        img = np.zeros((config.CAMERA_HEIGHT, config.CAMERA_WIDTH, 3), dtype=np.uint8)
        # Draw simulated background
        cv2.putText(img, "DEVELOPMENT SIMULATION FRAME", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        # Moving yellow ball in HSV spectrum
        cx = int(320 + 150 * np.sin(step * 0.1))
        cy = int(240 + 100 * np.cos(step * 0.1))
        cv2.circle(img, (cx, cy), 20, (0, 255, 255), -1)
        return img

    def stop(self):
        self.is_running = False
        self.is_online = False
        if self.cap:
            self.cap.release()
            self.cap = None
        print("[CameraStream] Camera stopped.")
