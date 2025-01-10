import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np

class FaceTracker:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.face_detector = FaceMeshDetector(maxFaces=1)
        self.focal_length = 530  # Calibrated focal length
        self.real_world_width = 6.3  # Distance between eyes in cm
        
    def get_face_distance(self):
        success, frame = self.video_capture.read()
        if not success:
            return None
            
        frame, face_mesh = self.face_detector.findFaceMesh(frame, draw=False)
        
        if not face_mesh:
            return None
            
        face_points = face_mesh[0]
        left_eye_point = face_points[145]
        right_eye_point = face_points[374]
        
        pixel_distance, _ = self.face_detector.findDistance(left_eye_point, right_eye_point)
        
        distance = (self.real_world_width * self.focal_length) / pixel_distance
        return distance
        
    def release(self):
        self.video_capture.release()
        cv2.destroyAllWindows()