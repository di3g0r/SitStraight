import tkinter as tk
from tkinter import messagebox
import cv2
import time
import numpy as np
from face_tracker import FaceTracker
from posture_monitor import PostureMonitor
from config import CALIBRATION_TIME, DISTANCE_THRESHOLD

class SitStraightApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SitStraight")
        self.root.geometry("400x200")
        
        self.face_tracker = FaceTracker()
        self.posture_monitor = PostureMonitor()
        
        self.setup_ui()
        self.calibration_done = False
        
    def setup_ui(self):
        # Main label
        self.status_label = tk.Label(
            self.root, 
            text="Welcome to SitStraight!\nPress Start to begin calibration",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=20)
        
        # Start button
        self.start_button = tk.Button(
            self.root,
            text="Start",
            command=self.start_monitoring,
            width=20,
            height=2
        )
        self.start_button.pack(pady=10)
        
        # Stop button
        self.stop_button = tk.Button(
            self.root,
            text="Stop",
            command=self.stop_monitoring,
            width=20,
            height=2,
            state=tk.DISABLED
        )
        self.stop_button.pack(pady=10)
        
    def start_monitoring(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Please sit straight.\nCalibrating your position...")
        
        # Start calibration
        self.root.after(100, self.calibration_phase)
        
    def calibration_phase(self):
        if not self.calibration_done:
            success = self.posture_monitor.calibrate(self.face_tracker)
            if success:
                self.calibration_done = True
                self.status_label.config(text="Calibration complete!\nMonitoring your posture...")
                self.monitoring_phase()
            else:
                messagebox.showerror("Error", "Couldn't detect face during calibration. Please try again.")
                self.stop_monitoring()
    
    def monitoring_phase(self):
        if not self.calibration_done:
            return
            
        current_distance = self.face_tracker.get_face_distance()
        if current_distance:
            is_correct = self.posture_monitor.check_posture(current_distance)
            if not is_correct:
                self.show_alert()
        
        # Continue monitoring if not stopped
        if self.calibration_done:
            self.root.after(100, self.monitoring_phase)
    
    def show_alert(self):
        self.status_label.config(text="⚠️ Sit Straight! ⚠️")
        self.root.after(2000, lambda: self.status_label.config(
            text="Monitoring your posture..." if self.calibration_done else "Welcome to SitStraight!"
        ))
    
    def stop_monitoring(self):
        self.calibration_done = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Welcome to SitStraight!\nPress Start to begin calibration")
        self.face_tracker.release()
        
    def run(self):
        self.root.mainloop()
        
    def on_closing(self):
        self.face_tracker.release()
        self.root.destroy()

if __name__ == "__main__":
    app = SitStraightApp()
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.run()