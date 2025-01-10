import time
import numpy as np
from config import CALIBRATION_TIME, DISTANCE_THRESHOLD

class PostureMonitor:
    def __init__(self):
        self.ideal_distance = None
        self.distances = []
        
    def calibrate(self, face_tracker):
        """Calibrate the ideal distance by taking measurements for CALIBRATION_TIME seconds"""
        start_time = time.time()
        self.distances = []
        
        while time.time() - start_time < CALIBRATION_TIME:
            distance = face_tracker.get_face_distance()
            if distance is not None:
                self.distances.append(distance)
            time.sleep(0.1)  # Small delay between measurements
            
        if len(self.distances) < 10:  # Require minimum number of measurements
            return False
            
        self.ideal_distance = np.mean(self.distances)
        return True
        
    def check_posture(self, current_distance):
        """Check if current posture is within acceptable range"""
        if self.ideal_distance is None:
            return True
            
        deviation = abs(current_distance - self.ideal_distance)
        return deviation <= DISTANCE_THRESHOLD