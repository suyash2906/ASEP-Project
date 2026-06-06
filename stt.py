"""Speech-to-Text module using Google Speech Recognition.

This module provides functionality to capture speech from a microphone
and convert it to text using the Google Speech Recognition API.
"""

from typing import Optional
import speech_recognition as sr

# import pyaudio  # Commented - use wheel install


def speech_to_text(timeout: int = 15, phrase_time_limit: int = 10) -> str:
    """Capture speech and convert to text using SpeechRecognition.

    Args:
        timeout (int): Maximum time to listen in seconds. Defaults to 15.
        phrase_time_limit (int): Maximum duration of a phrase in seconds. Defaults to 10.

    Returns:
        str: Transcribed text or error message if speech could not be recognized.

    Raises:
        No exceptions are raised; errors are caught and returned as strings.
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
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        print("Recognizing with Google...")
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        print("Sorry, could not understand - speak closer/louder")
        return "Audio unclear"
    except sr.RequestError as e:
        print(f"Google API error: {e}")
        return "API error"
    except sr.WaitTimeoutError:
        print("Timeout - no speech detected")
        return "Timeout - no speech"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error occurred"


if __name__ == "__main__":
    result = speech_to_text()
    print("Result:", result)
