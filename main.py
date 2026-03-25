"""
Main application for Hand Gesture Controlled YouTube Player.
Integrates hand tracking, gesture detection, and controls.
"""
import cv2
import time
import numpy as np
import sys

# Auto-install dependencies if missing
REQUIRED = ['opencv-python', 'mediapipe', 'pyautogui', 'numpy']
def install_missing():
    import importlib
    import subprocess
    for pkg in REQUIRED:
        try:
            importlib.import_module(pkg.split('-')[0])
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
install_missing()

from hand_tracking import HandTracker
from gesture_detection import GestureDetector
from controls import YouTubeController

def main():
    cap = cv2.VideoCapture(0)
    # Set camera resolution to a large rectangle (half screen, e.g., 1280x720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    tracker = HandTracker()
    detector = GestureDetector(confidence_threshold=0.7)
    controller = YouTubeController()
    prev_lm_list = None
    p_time = 0
    gesture = ""
    gesture_cooldown = 1.0
    gesture_time = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame = tracker.find_hands(frame, draw=True)
        lm_list = tracker.find_position(frame)
        detected_gesture = ""
        action_text = ""
        if lm_list:
            detected_gesture = detector.detect_gesture(lm_list, prev_lm_list)
            if detected_gesture != "Unknown" and (time.time() - gesture_time) > gesture_cooldown:
                controller.trigger(detected_gesture)
                gesture = detected_gesture
                gesture_time = time.time()
            # Map gesture to action text for feedback
            if detected_gesture == "Fist":
                action_text = "Pause"
            elif detected_gesture == "Open Hand":
                action_text = "Play/Resume"
            elif detected_gesture == "Two Fingers Up":
                action_text = "Fast Forward"
            elif detected_gesture == "Two Fingers Down":
                action_text = "Rewind"
            else:
                action_text = ""
        prev_lm_list = lm_list
        # FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time
        # Overlay gesture, action, and FPS
        cv2.putText(frame, f'Gesture: {gesture}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, f'Action: {action_text}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,128,255), 2)
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.imshow('Hand Gesture YouTube Controller', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
