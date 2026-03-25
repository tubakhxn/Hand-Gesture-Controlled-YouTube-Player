"""
Gesture detection module.
Detects gestures based on hand landmarks.
"""
import numpy as np

class GestureDetector:
    def __init__(self, confidence_threshold=0.7):
        self.confidence_threshold = confidence_threshold

    def fingers_up(self, lm_list):
        # Returns a list of 5 ints: 1 if finger is up, 0 if down
        if not lm_list or len(lm_list) < 21:
            return [0, 0, 0, 0, 0]
        tips = [4, 8, 12, 16, 20]
        fingers = []
        # Thumb: tip x > IP x (for right hand, webcam is mirrored)
        fingers.append(1 if lm_list[tips[0]][1] > lm_list[tips[0] - 1][1] + 20 else 0)
        # Index, Middle, Ring, Pinky: tip y < pip y (up)
        for i, tip in enumerate(tips[1:], start=1):
            fingers.append(1 if lm_list[tip][2] < lm_list[tip - 2][2] - 20 else 0)
        return fingers

    def detect_gesture(self, lm_list, prev_lm_list=None):
        # Returns gesture name string
        fingers = self.fingers_up(lm_list)
        # Fist: all fingers down
        if fingers == [0, 0, 0, 0, 0]:
            return "Fist"  # Pause
        # Open hand: all fingers up
        if fingers == [1, 1, 1, 1, 1]:
            return "Open Hand"  # Play/Resume
        # Two fingers up (index + middle up, rest down)
        if fingers == [0, 1, 1, 0, 0]:
            return "Two Fingers Up"  # Fast Forward
        # Two fingers down (index + middle down, ring+pinky+thumb up)
        if fingers == [1, 0, 0, 1, 1]:
            return "Two Fingers Down"  # Rewind
        # Allow for some flexibility: if only index+middle up, rest down
        if fingers == [0, 1, 1, 0, 0]:
            return "Two Fingers Up"
        # If only index+middle down, rest up
        if fingers == [1, 0, 0, 1, 1]:
            return "Two Fingers Down"
        # If hand is open but not all fingers detected, treat as open hand
        if sum(fingers) >= 4:
            return "Open Hand"
        return "Unknown"