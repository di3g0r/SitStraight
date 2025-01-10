import tkinter as tk
from tkinter import messagebox
import pystray
from PIL import Image, ImageTk
import winsound
import threading
import os
import time
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
        self.is_alert_active = False
        self.alert_thread = None
        
        # Create system tray icon
        self.setup_system_tray()
        
        # Flag to track if window is minimized
        self.is_minimized = False
        
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

    def setup_system_tray(self):
        # Create a simple icon (you should replace this with your own icon)
        icon = Image.new('RGB', (64, 64), color='blue')
        self.tray_icon = pystray.Icon("SitStraight", icon, "SitStraight", menu=self.create_tray_menu())
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def create_tray_menu(self):
        return pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Exit", self.on_closing)
        )

    def show_window(self):
        self.root.deiconify()
        self.is_minimized = False

    def minimize_to_tray(self):
        self.root.withdraw()
        self.is_minimized = True

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
            if not is_correct and not self.is_alert_active:
                self.show_alert()
            elif is_correct and self.is_alert_active:
                self.stop_alert()
        
        # Continue monitoring if not stopped
        if self.calibration_done:
            self.root.after(100, self.monitoring_phase)

    def play_alert_sound(self):
        try:
            # Play custom sound file with SND_ASYNC and SND_LOOP for continuous playback
            sound_file = os.path.join(os.path.dirname(__file__), "alert.wav")
            winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        except Exception as e:
            print(f"Error playing sound: {e}")
            # Fallback to system sound if custom sound fails
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)

    def show_alert(self):
        # Start alert only if not already active
        if not self.is_alert_active:
            self.is_alert_active = True
            # Update status label
            self.status_label.config(text="⚠️ Sit Straight! ⚠️")
            # Start sound alert
            self.play_alert_sound()
            # Show system notification if window is minimized
            if self.is_minimized:
                self.tray_icon.notify(
                    "SitStraight Alert",
                    "Please adjust your posture!"
                )

    def stop_alert(self):
        self.is_alert_active = False
        # Stop any currently playing sound
        winsound.PlaySound(None, 0)
        self.status_label.config(
            text="Monitoring your posture..." if self.calibration_done else "Welcome to SitStraight!"
        )

    def stop_monitoring(self):
        self.calibration_done = False
        self.is_alert_active = False
        if self.alert_thread and self.alert_thread.is_alive():
            self.alert_thread.join(timeout=1)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Welcome to SitStraight!\nPress Start to begin calibration")
        self.face_tracker.release()

    def on_closing(self):
        self.is_alert_active = False
        if self.alert_thread and self.alert_thread.is_alive():
            self.alert_thread.join(timeout=1)
        self.face_tracker.release()
        self.tray_icon.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SitStraightApp()
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.run()