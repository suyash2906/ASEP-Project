import speech_recognition as sr
# import pyaudio  # Commented - use wheel install

def speech_to_text():
    """
    Capture speech and convert to text using SpeechRecognition.
    """
    recognizer = sr.Recognizer()
    
    # List mics only once (clean output)
    print("Available microphones:")
    mics = sr.Microphone.list_microphone_names()
    for i, name in enumerate(mics[:5]):  # Show top 5 only
        print(f"  {i}: {name}")
    
    microphone = sr.Microphone(device_index=0)  # Default mic
    
    try:
        with microphone as source:
            print("Adjusting for ambient noise... Speak in 3s...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
        
        print("🎤 Listening... Speak LOUD & CLEAR (10s)")
        with microphone as source:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
        
        print("Recognizing with Google...")
        text = recognizer.recognize_google(audio)
        return text
        
    except sr.UnknownValueError:
        print("Sorry, could not understand - speak closer/louder")
        return "Audio unclear"
    except sr.RequestError as e:
        print("Google API error:", e)
        return "API error"
    except sr.WaitTimeoutError:
        return "Timeout - no speech"
        
    except sr.WaitTimeoutError:
        return "No speech detected"
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        print(f"STT Error: {e}")
        return "STT service error"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error occurred"

if __name__ == "__main__":
    result = speech_to_text()
    print("Result:", result)

