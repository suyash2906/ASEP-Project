import cv2
import mediapipe as mp
import numpy as np
import time

# Full ASL Alphabet mapping by simplified landmark patterns
ASL_MAP = {
    # Fist variations
    0: "A",
    # Index variations  
    1: "J L",
    # V variations
    2: "U V",
    # 3 fingers
    3: "E W",
    # 4 fingers
    4: "H Q",
    # Open hand
    5: "B HELLO"
}

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

def advanced_gesture_recognition():
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8
    )
    
    cap = cv2.VideoCapture(0)
    print("ASL Gesture → Letter Recognition (hold gesture 2s). 'q' to quit.")
    
    gesture_start_time = 0
    stable_gesture = None
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        gesture_text = "Show ASL gesture"
        if results.multi_hand_landmarks:
            hand_lms = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            
            finger_count = count_fingers(hand_lms, mp_hands)
            current_gesture = ASL_MAP.get(finger_count, f"{finger_count} fingers")
            
            # Stability detection (hold 2s)
            if current_gesture == stable_gesture:
                if time.time() - gesture_start_time > 2.0:
                    gesture_text = f"ASL: {current_gesture} ✓"
            else:
                stable_gesture = current_gesture
                gesture_start_time = time.time()
                gesture_text = f"Holding... {current_gesture}"
        else:
            stable_gesture = None
        
        cv2.putText(img, gesture_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        cv2.imshow("ASL Gesture → Letter", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def count_fingers(hand_landmarks, mp_hands):
    fingers = []
    # Thumb
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
        fingers.append(1)
    else:
        fingers.append(0)
    # Other fingers
    for tip, pip in [(4,3), (8,6), (12,10), (16,14)]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)

if __name__ == "__main__":
    advanced_gesture_recognition()

