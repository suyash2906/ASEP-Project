import os
import sys
import pygame
from tts import text_to_speech
from stt import speech_to_text
from text_to_sign import text_to_sign
from hand_detection import detect_hands
from gesture_to_text import gesture_to_text
from menu import show_menu

def main():
    try:
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
    except:
        print("Mixer init failed - TTS will use file fallback")
        
    while True:
        choice = show_menu()
        if choice == '1':
            text = input("Enter text for TTS: ")
            text_to_speech(text)
        elif choice == '2':
            text = speech_to_text()
            print("Transcribed:", text)
        elif choice == '3':
            text = input("Enter text for Sign Language: ")
            text_to_sign(text)
        elif choice == '4':
            text = speech_to_text()
            print("Speech to Sign:", text)
            text_to_sign(text)
        elif choice == '5':
            detect_hands()
        elif choice == '0':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

