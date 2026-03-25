"""
Hand tracking module using MediaPipe Tasks API (0.10+).
Detects and tracks hand landmarks in real-time.
"""
import cv2
import numpy as np
import os
import urllib.request
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarker, HandLandmarkerOptions, HandLandmarkerResult
from mediapipe.tasks.python.vision.core.image import Image as MpImage
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode

class HandTracker:
    def __init__(self, max_num_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.model_path = 'hand_landmarker.task'
        if not os.path.exists(self.model_path):
            url = 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'
            urllib.request.urlretrieve(url, self.model_path)
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionTaskRunningMode.IMAGE,
            num_hands=max_num_hands,
            min_hand_detection_confidence=detection_confidence,
            min_hand_presence_confidence=tracking_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.detector = HandLandmarker.create_from_options(options)
        self.last_result = None

    def find_hands(self, img, draw=True):
        mp_image = MpImage(image_format=1, data=img)  # 1 = SRGB
        self.last_result = self.detector.detect(mp_image)
        if draw and self.last_result.hand_landmarks:
            for hand_landmarks in self.last_result.hand_landmarks:
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * img.shape[1]), int(lm.y * img.shape[0])
                    cv2.circle(img, (cx, cy), 5, (0,255,0), -1)
        return img

    def find_position(self, img, hand_no=0):
        lm_list = []
        if self.last_result and self.last_result.hand_landmarks:
            if hand_no < len(self.last_result.hand_landmarks):
                hand = self.last_result.hand_landmarks[hand_no]
                h, w, _ = img.shape
                for id, lm in enumerate(hand):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((id, cx, cy))
        return lm_list
