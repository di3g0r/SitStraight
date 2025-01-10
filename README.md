# SitStraight Application Documentation

## Overview
SitStraight is a desktop application designed to help users maintain good posture while working at their computer. The application uses your webcam to monitor the distance between your face and the screen, alerting you when you deviate from your ideal posture position.

## Features
- Real-time posture monitoring using webcam
- Initial calibration period to determine ideal posture
- Continuous monitoring with audio and visual alerts
- System tray integration for background operation
- Desktop notifications when minimized
- Custom alert sounds

## Requirements

### Hardware Requirements
- Webcam
- Audio output device (speakers or headphones)
- Windows operating system

### Software Requirements
To run SitStraight, you need Python and several packages. Here's how to set everything up:

1. Install Python 3.10 or later from [python.org](https://python.org)

2. Create and activate a virtual environment:
```bash
python -m venv myenv
myenv\Scripts\activate
```

3. Install required packages:
```bash
pip install opencv-python
pip install cvzone
pip install mediapipe
pip install pillow
pip install pystray
pip install numpy
```

4. Place an audio file named `alert.wav` in the project directory for custom alerts

## Project Structure
```
SitStraight/
├── main.py              # Main application file
├── face_tracker.py      # Face detection and distance measurement
├── posture_monitor.py   # Posture monitoring and calibration
├── config.py           # Configuration settings
└── alert.wav           # Custom alert sound
```

## How It Works

1. **Initial Calibration**
   - When you start the app, sit in your ideal posture
   - Click "Start" to begin calibration
   - The app measures your ideal distance for 5 seconds

2. **Continuous Monitoring**
   - After calibration, the app monitors your position
   - If you move ±1cm from the ideal distance, you'll receive alerts
   - Audio alerts play continuously until you return to the correct position

3. **Background Operation**
   - The app can be minimized to the system tray
   - You'll receive desktop notifications when minimized
   - Audio alerts continue even when minimized

## Usage Instructions

1. Launch the application by running `main.py`
2. Ensure your webcam has a clear view of your face
3. Sit in your ideal posture position
4. Click "Start" to begin calibration
5. Maintain your position during the 5-second calibration
6. The app will now monitor your posture
7. Minimize to tray if desired

## Additional Notes
- The application uses the distance between your eyes to calculate your position
- The alert threshold is set to ±1cm from your calibrated position
- You can customize the alert sound by replacing `alert.wav` with any WAV file
