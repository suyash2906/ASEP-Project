"""Gesture-to-Text module using hand gesture recognition.

This module provides functionality to detect hand gestures via camera and
convert them to text based on finger counts and hand positions.
"""

from typing import List, Dict
from collections import deque

import cv2
import mediapipe as mp

# Simple gesture mapping based on finger counts
GESTURE_MAP: Dict[int, str] = {0: "FIST", 1: "INDEX", 2: "VICTORY", 5: "HELLO"}


def count_fingers(hand_landmarks, mp_hands) -> int:
    """Count raised fingers from hand landmarks.

    Args:
        hand_landmarks: MediaPipe hand landmarks object.
        mp_hands: MediaPipe hands solution.

    Returns:
        int: Number of raised fingers (0-5).
    """
    fingers: List[int] = []

    # Thumb
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[
        mp_hands.HandLandmark.THUMB_IP
    ].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers
    for tip, pip in [(4, 3), (8, 6), (12, 10), (16, 14)]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)


def gesture_to_text(duration: int = 5) -> str:
    """Detect simple gestures (finger count based) and map to text.

    Args:
        duration (int): Duration to detect gestures in seconds. Defaults to 5.

    Returns:
        str: Detected gesture text or "NONE" if no gesture detected.

    Example:
        >>> gesture = gesture_to_text(duration=5)
        >>> print(f"Detected: {gesture}")
    """
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )

    cap = cv2.VideoCapture(0)
    gesture_history: deque = deque(maxlen=30)  # 1 second at 30fps
    start_time = cv2.getTickCount()

    print("Show gesture for 5 seconds. Press 'q' to quit early.")

    try:
        while (cv2.getTickCount() - start_time) / cv2.getTickFrequency() < duration:
            success, img = cap.read()
            if not success:
                break

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            gesture = "NONE"
            if results.multi_hand_landmarks:
                for hand_lms in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

                    finger_count = count_fingers(hand_lms, mp_hands)
                    gesture = GESTURE_MAP.get(finger_count, f"{finger_count}_FINGERS")
                    gesture_history.append(gesture)

            # Show most common gesture
            cv2.putText(
                img,
                f"Gesture: {gesture}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            cv2.imshow("Gesture Detection", img)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()

    if gesture_history:
        most_common = max(set(gesture_history), key=gesture_history.count)
        print(f"Detected gesture: {most_common}")
        return most_common
    else:
        print("No gesture detected")
        return "NONE"


if __name__ == "__main__":
    result = gesture_to_text()
    print("Final result:", result)
