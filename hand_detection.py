import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import pygame

# Comprehensive ASL gesture mapping by finger count
GESTURE_MAP = {
    0: "FIST (A-like)",
    1: "INDEX POINT", 
    2: "VICTORY (V)",
    3: "THREE (3/W)",
    4: "FOUR (4)",
    5: "HELLO (H)",
}

def count_fingers(hand_landmarks, mp_hands):
    """
    Count raised fingers from hand landmarks.
    """
    fingers = []
    
    # Thumb
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Other 4 fingers
    for tip, pip in [(4,3), (8,6), (12,10), (16,14)]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return sum(fingers)

def detect_hands():
    """
    Real-time hand detection using MediaPipe.
    """
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    
    cap = cv2.VideoCapture(0)
    
    pygame.mixer.init()
    
    print("Hand detection + Basic Gesture Recognition. Press 'q' to quit.")
    
    while True:
        success, img = cap.read()
        if not success:
            break
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        gesture_text = "No hand"
        if results.multi_hand_landmarks:
            gesture_texts = []
            for hand_lms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
                
                finger_count = count_fingers(hand_lms, mp_hands)
                gesture = GESTURE_MAP.get(finger_count, f"{finger_count} fingers")
                gesture_texts.append(gesture)
            
            gesture_text = "/".join(gesture_texts[:2])  # Show up to 2 hands
            num_hands = len(results.multi_hand_landmarks)
            print(f"{num_hands} hands: {gesture_text}")
        else:
            print("No hands")
        
        # Display on video
        cv2.putText(img, gesture_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imshow("Hand + Gesture Detection", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Hand detection stopped.")

if __name__ == "__main__":
    detect_hands()

