import cv2
import threading
import time
from typing import Optional

class CameraStream:
    def __init__(self, camera_index: int = 0, width: int = 640, height: int = 480):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.frame = None
        self.lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> bool:
        """Starts the camera capture thread."""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print(f"[CameraStream] Error: Could not open camera at index {self.camera_index}")
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        self.is_running = True
        self._thread = threading.Thread(target=self._update_loop, daemon=True)
        self._thread.start()
        print(f"[CameraStream] Camera {self.camera_index} started ({self.width}x{self.height}).")
        return True

    def _update_loop(self):
        while self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
            else:
                time.sleep(0.01)

    def get_frame(self):
        """Returns the latest captured frame."""
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        """Stops the camera capture thread and releases resources."""
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=1.0)
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print("[CameraStream] Camera released.")
