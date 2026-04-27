from gtts import gTTS
import pygame
import io
import os

def text_to_speech(text, lang='en'):
    """
    Convert text to speech using gTTS and play using pygame.
    """
    try:
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
            
        pygame.mixer.quit()
        print(f"TTS completed: {text[:50]}...")
    except Exception as e:
        print(f"TTS Error: {e}")
        # Fallback: save to file
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save("temp_speech.mp3")
            os.system("start temp_speech.mp3")  # Windows default player
            print("Saved temp_speech.mp3 - opened in default player")
        except:
            print("TTS fully failed")

if __name__ == "__main__":
    text_to_speech("Hello, this is text to speech test.")

