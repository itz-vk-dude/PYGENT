import cv2
import numpy as np
from typing import Dict, Any, List

class ObjectDetector:
    """
    OpenCV HSV Color Segmentation + Haar Cascade Face Detector.
    Detects relevant objects, humans, centers, bounding regions, and confidence scores.
    """
    def __init__(self, color_lower: tuple = (29, 86, 6), color_upper: tuple = (64, 255, 255)):
        self.color_lower = np.array(color_lower, dtype="uint8")
        self.color_upper = np.array(color_upper, dtype="uint8")
        
        # Load OpenCV Haar Cascades
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def set_color_range(self, lower: tuple, upper: tuple):
        self.color_lower = np.array(lower, dtype="uint8")
        self.color_upper = np.array(upper, dtype="uint8")

    def detect(self, frame: np.ndarray) -> Dict[str, Any]:
        if frame is None:
            return {"detected": False, "person_present": False, "x": 0.0, "y": 0.0, "radius": 0.0, "objects": [], "confidence": 0.0}

        objects_list: List[Dict[str, Any]] = []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect Face / Person
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        person_present = len(faces) > 0
        if person_present:
            for (fx, fy, fw, fh) in faces:
                objects_list.append({
                    "type": "human",
                    "name": "Person Face",
                    "bbox": [int(fx), int(fy), int(fw), int(fh)],
                    "center": [float(fx + fw / 2.0), float(fy + fh / 2.0)],
                    "confidence": 0.90
                })

        # Detect Object via HSV
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.color_lower, self.color_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        ball_detected = False
        bx, by, br = 0.0, 0.0, 0.0
        confidence = 0.0

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((cx, cy), radius) = cv2.minEnclosingCircle(c)
            if radius > 5:
                ball_detected = True
                bx, by, br = float(cx), float(cy), float(radius)
                confidence = min(1.0, float(radius) / 50.0)
                objects_list.append({
                    "type": "object",
                    "name": "Tracked Object",
                    "center": [bx, by],
                    "radius": br,
                    "bbox": [int(bx - br), int(by - br), int(2 * br), int(2 * br)],
                    "confidence": confidence
                })

        main_x = bx if ball_detected else (objects_list[0]["center"][0] if person_present else 0.0)
        main_y = by if ball_detected else (objects_list[0]["center"][1] if person_present else 0.0)

        return {
            "detected": ball_detected,
            "person_present": person_present,
            "x": main_x,
            "y": main_y,
            "radius": br,
            "objects": objects_list,
            "confidence": confidence if ball_detected else (0.85 if person_present else 0.0)
        }
