"""
Controls module.
Maps gestures to YouTube keyboard shortcuts using pyautogui.
"""
import pyautogui
import time

class YouTubeController:
    def __init__(self):
        self.last_action_time = 0
        self.cooldown = 1.0  # seconds

    def _can_trigger(self):
        return (time.time() - self.last_action_time) > self.cooldown

    def trigger(self, gesture):
        if not self._can_trigger():
            return
        if gesture == "Fist":
            pyautogui.press('space')  # Pause
        elif gesture == "Open Hand":
            pyautogui.press('space')  # Play/Resume
        elif gesture == "Two Fingers Up":
            pyautogui.press('right')  # Fast Forward
        elif gesture == "Two Fingers Down":
            pyautogui.press('left')   # Rewind
        self.last_action_time = time.time()
