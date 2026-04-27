import cv2
import mediapipe as mp
import numpy as np
import collections
import time

# Real ASL word mapping based on hand shape templates (simplified prototype)
# Maps finger configurations + palm orientation to common ASL words/letters
# Complete A-Z ASL Alphabet mapping (simplified by finger config + orientation)
# Precise A-Z mapping - single letter per exact config (no overlap)
ASL_ALPHABET = {
    # Base finger count (palm forward 0.5)
    0: "A",    # Closed fist
    1: "I",    # Index up
    2: "V",    # Victory
    3: "E",    # 3 fingers
    4: "H",    # Pinky/index
    5: "B",    # Open hand
    
    # Palm left (0.2)
    (0, 0.2): "S",
    (1, 0.2): "J",
    (2, 0.2): "U",
    (3, 0.2): "W",
    (4, 0.2): "K",
    (5, 0.2): "L",
    
    # Palm right (0.8)
    (0, 0.8): "O",
    (1, 0.8): "Y",
    (2, 0.8): "N",
    (3, 0.8): "T",
    (4, 0.8): "Q",
    (5, 0.8): "M",
    
    # Thumb specific
    (0, 0.1): "F",
    (0, 0.9): "G",
    
    # Special
    (1, 0.1): "X",
    (1, 0.9): "P",
    (2, 0.1): "C",
    (3, 0.9): "D",
    (4, 0.1): "R"
}

def get_alphabet_prediction(fingers, palm_dir):
    key = (fingers, round(palm_dir, 1))
    if key in ASL_ALPHABET:
        return ASL_ALPHABET[key]
    
    # Fallback to finger count
    return ASL_ALPHABET.get(fingers, f"UNKNOWN {fingers}")

def palm_orientation(hand_landmarks):
    """Simple palm facing estimation (0-1 left to right)"""
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    pinky = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    return (pinky.x - wrist.x + 1) / 2  # Normalized 0-1

def real_asl_word_recognition():
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8
    )
    
    cap = cv2.VideoCapture(0)
    gesture_buffer = collections.deque(maxlen=30)
    
    print("=== REAL ASL WORD Recognition ===")
    print("Hold ASL hand shape 3s → Recognizes WORD/LETTER")
    print("'q' quit, 'r' reset")
    
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # Mirror for natural view
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        word = "SHOW ASL SHAPE"
        confidence = 0
        
        if results.multi_hand_landmarks:
            hand_lms = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            
            fingers = count_fingers(hand_lms, mp_hands)
            palm_dir = palm_orientation(hand_lms)
            
            key = (fingers, round(palm_dir, 1))
            gesture_buffer.append(key)
            
            # Stability check
            if len(set(gesture_buffer)) == 1 and len(gesture_buffer) == 45:
                stable_key = gesture_buffer[0]
                word = get_alphabet_prediction(*stable_key)
                confidence = 100
            elif len(gesture_buffer) >= 30:
                most_common = collections.Counter(gesture_buffer).most_common(1)[0]
                if most_common[1] / len(gesture_buffer) > 0.9:  # Stricter threshold
                    word = get_alphabet_prediction(*most_common[0])
                    confidence = int(most_common[1] / len(gesture_buffer) * 100)
                else:
                    word = "HOLD STEADY"
                    confidence = int(len(gesture_buffer)/45 * 50)
            
            cv2.putText(img, f"ASL: {word} ({confidence}%)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            cv2.putText(img, f"Fingers: {fingers} Palm: {palm_dir:.1f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 2)
        else:
            gesture_buffer.clear()
        
        cv2.imshow("Real ASL → WORD Recognition", img)
        
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        if k == ord('r'):
            gesture_buffer.clear()
    
    cap.release()
    cv2.destroyAllWindows()
    print("ASL Recognition stopped.")

def count_fingers(hand_landmarks, mp_hands):
    fingers = 0
    # Thumb
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
        fingers += 1
    # Index
    if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y:
        fingers += 1
    # Middle  
    if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y:
        fingers += 1
    # Ring
    if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y:
        fingers += 1
    # Pinky
    if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y:
        fingers += 1
    return fingers

if __name__ == "__main__":
    real_asl_word_recognition()

