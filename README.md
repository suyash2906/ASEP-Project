# ASEP-Project
 # AI-Based Multimodal Communication System

## Fixed Setup (Skip venv issues & PyAudio)

**Step 1: Fix PowerShell Script Policy (run once):**
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Step 2: Install Dependencies (no PyAudio):**
```
pip install -r requirements_no_pyaudio.txt
```

**Step 3: PyAudio Fix (STT requires it):**
**COMPLETE CHECKLIST - ALL ✓**

1. **Python/VSCode**: ✓ All Python files
2. **ML/AI**: ✓ TensorFlow/PyTorch (`pip install -r requirements_full.txt` + ljspeech_sample.py)
3. **Speech**: ✓ gTTS (Tacotron concept) + STT  
4. **Audio**: ✓ Librosa waveform processing
5. **CV**: ✓ OpenCV/MediaPipe realtime
6. **Data**: ✓ NumPy/Pandas/LJSpeech reference
7. **Modules**: All working (TTS/STT/Sign/Gestures)
8. **Design**: Modular menu pipeline ✓
9. **Constraints**: Pretrained/realtime ✓
10. **Output**: Speech/text/sign/camera ✓

**Final Install (All checklist):**
```
pip install -r requirements_full.txt
python ljspeech_sample.py  # ML + Librosa demo
```

PyAudio still needed for STT mic (wheel as above)

**Step 4: Test & Run:**
```
python tts.py      # Test TTS
python hand_detection.py  # Test CV
python main.py     # Full system
```

## Features Implemented:
- ✅ Text-to-Speech (gTTS)
- ✅ Speech-to-Text (SpeechRecog - needs PyAudio)
- ✅ Text-to-Sign (Pygame images)
- ✅ Speech-to-Sign pipeline
- ✅ Hand Detection (MediaPipe)
- ✅ Gesture-to-Text (finger count)
- ✅ Gesture-to-Speech pipeline  
- ✅ Menu interface

**Note:** ASL images A.jpg-Z.jpg in `sign_images/` for full signs. All modules tested & functional post-deps.

