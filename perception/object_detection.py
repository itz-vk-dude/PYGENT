import cv2
import numpy as np
from typing import Dict, Any

class ObjectDetector:
    def __init__(self, color_lower: tuple = (29, 86, 6), color_upper: tuple = (64, 255, 255)):
        """
        Initializes HSV color threshold range for object detection + OpenCV Haar Cascades for Person / Face.
        """
        self.color_lower = np.array(color_lower, dtype="uint8")
        self.color_upper = np.array(color_upper, dtype="uint8")
        
        # Load OpenCV default face and upperbody cascade classifiers
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

    def set_color_range(self, lower: tuple, upper: tuple):
        self.color_lower = np.array(lower, dtype="uint8")
        self.color_upper = np.array(upper, dtype="uint8")

    def detect(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Detects ball object and human presence (person/face) in webcam frame.
        """
        if frame is None:
            return {"detected": False, "person_present": False, "x": 0.0, "y": 0.0, "radius": 0.0, "objects": []}

        objects_list = []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect Face / Person
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        person_present = len(faces) > 0
        if person_present:
            for (fx, fy, fw, fh) in faces:
                objects_list.append({
                    "name": "Person Face",
                    "bbox": [int(fx), int(fy), int(fw), int(fh)],
                    "center": [float(fx + fw/2), float(fy + fh/2)]
                })

        # Detect Ball/Object via HSV
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.color_lower, self.color_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        ball_detected = False
        bx, by, br = 0.0, 0.0, 0.0

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((cx, cy), radius) = cv2.minEnclosingCircle(c)
            if radius > 5:
                ball_detected = True
                bx, by, br = float(cx), float(cy), float(radius)
                objects_list.append({
                    "name": "Ball Object",
                    "center": [bx, by],
                    "radius": br
                })

        return {
            "detected": ball_detected,
            "person_present": person_present,
            "x": bx if ball_detected else (objects_list[0]["center"][0] if person_present else 0.0),
            "y": by if ball_detected else (objects_list[0]["center"][1] if person_present else 0.0),
            "radius": br,
            "objects": objects_list
        }

