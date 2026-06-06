# ASEP-Project
# AI-Based Multimodal Communication System

A comprehensive Python application that enables communication across multiple modalities including Text-to-Speech, Speech-to-Text, Sign Language, and Gesture Recognition. Ideal for bridging communication gaps for people with different abilities.

## Features Implemented

- ✅ **Text-to-Speech (TTS)** - Convert text to natural-sounding speech using gTTS
- ✅ **Speech-to-Text (STT)** - Transcribe spoken words to text using Google Speech Recognition
- ✅ **Text-to-Sign Language** - Display sign language representations for text input
- ✅ **Speech-to-Sign Pipeline** - Convert speech directly to sign language
- ✅ **Hand Detection** - Real-time hand tracking using MediaPipe
- ✅ **Gesture-to-Text** - Recognize hand gestures and convert to text
- ✅ **Gesture-to-Speech Pipeline** - Convert gestures to spoken audio
- ✅ **Menu Interface** - Interactive CLI for testing individual modules
- ✅ **GUI Application** - User-friendly graphical interface with threading

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended for smooth operation)
- **Processor**: Dual-core or higher
- **Microphone**: Required for STT functionality
- **Webcam**: Required for hand detection and gesture recognition

### Supported Operating Systems
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/suyash2906/ASEP-Project.git
cd ASEP-Project
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
.\\venv\\Scripts\\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

#### Option A: Basic Installation (Recommended for most users)

```bash
pip install -r requirements.txt
```

#### Option B: Full Installation (with development tools)

```bash
pip install -r requirements-dev.txt
```

### Step 4: Handle PyAudio (STT Requirement)

**For Windows:**
```bash
# Download appropriate wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then install:
pip install PyAudio-0.2.11-cp311-cp311-win_amd64.whl  # Replace with your Python version
```

**For macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**For Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Step 5: Prepare Sign Language Images

Create a `sign_images/` directory in the project root:

```bash
mkdir sign_images
```

Add sign language images for letters A-Z (named `A.jpg`, `B.jpg`, etc.) and a space gesture image (`space.jpg`).

## Usage

### GUI Application (Recommended)

```bash
python gui_app.py
```

The GUI provides easy access to all features:
- Click buttons to trigger each functionality
- Enter text in the input field for TTS and Sign Language
- Results from STT are automatically displayed in the text field
- Activity log shows all operations with timestamps

### Command Line Interface

```bash
python main.py
```

Follow the on-screen menu to select features:
1. Text to Speech
2. Speech to Text
3. Text to Sign Language
4. Speech to Sign Language
5. Hand Detection

### Test Individual Modules

**Text-to-Speech:**
```bash
python tts.py
```

**Speech-to-Text:**
```bash
python stt.py
```

**Gesture Recognition:**
```bash
python gesture_to_text.py
```

**Text-to-Sign Language:**
```bash
python text_to_sign.py
```

## Project Structure

```
ASEP-Project/
├── main.py                 # CLI entry point
├── gui_app.py             # GUI application
├── tts.py                 # Text-to-Speech module
├── stt.py                 # Speech-to-Text module
├── text_to_sign.py        # Text-to-Sign Language module
├── gesture_to_text.py     # Gesture recognition module
├── hand_detection.py      # Hand detection using MediaPipe
├── menu.py                # Menu interface
├── requirements.txt       # Core dependencies
├── requirements-dev.txt   # Development dependencies
├── pyproject.toml         # Python package configuration
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore             # Git ignore rules
├── .github/
│   └── workflows/         # CI/CD workflows
│       ├── tests.yml      # Automated tests
│       └── code-quality.yml  # Code quality checks
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_stt.py
│   ├── test_text_to_sign.py
│   └── test_gesture_to_text.py
└── sign_images/           # Directory for ASL images
    ├── A.jpg
    ├── B.jpg
    └── ... (A-Z)
```

## Troubleshooting

### Audio Issues

**Problem:** "No microphone found" or STT not working

**Solution:**
1. Verify microphone is connected and recognized by OS
2. Check microphone permissions in system settings
3. Try reinstalling PyAudio: `pip uninstall pyaudio && pip install pyaudio`
4. On Windows, download the correct wheel for your Python version

**Problem:** Speaker output not working

**Solution:**
1. Check system volume is not muted
2. Verify audio device is set as default in system settings
3. Test with a different audio player to confirm speakers work

### Camera Issues

**Problem:** "Camera not found" for hand detection

**Solution:**
1. Verify webcam is connected
2. Check camera permissions in system settings (especially on macOS)
3. Ensure no other application is using the camera
4. Try restarting the application

### ImportError Issues

**Problem:** Module not found errors

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall requirements: `pip install --upgrade -r requirements.txt`
3. Check Python version: `python --version` (should be 3.8+)

### PyAudio Installation Issues

**Windows Users:**
- Download pre-built wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Match your Python version (3.9, 3.10, 3.11, etc.)
- Install wheel file directly

**macOS/Linux Users:**
- Install PortAudio development files first
- Then install PyAudio via pip

## Development

### Running Tests

```bash
pytest tests/
```

Generate coverage report:
```bash
pytest tests/ --cov=. --cov-report=html
```

### Code Quality

**Format code:**
```bash
black .
```

**Check style:**
```bash
flake8 .
```

**Type checking:**
```bash
mypy .
```

## Architecture

### Module Overview

- **tts.py**: Uses gTTS for text-to-speech conversion
- **stt.py**: Uses SpeechRecognition with Google API for speech-to-text
- **text_to_sign.py**: Displays sign language images using Pygame
- **gesture_to_text.py**: Detects hand gestures using MediaPipe
- **hand_detection.py**: Real-time hand tracking and visualization
- **gui_app.py**: Tkinter-based GUI with threading support
- **main.py**: CLI menu-driven interface

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| SpeechRecognition | 3.10.0 | Speech-to-text conversion |
| gTTS | 2.4.0 | Text-to-speech conversion |
| opencv-python | 4.8.1.78 | Computer vision operations |
| mediapipe | 0.10.9 | Hand detection and tracking |
| pygame | 2.5.2 | Audio playback and graphics |
| Pillow | 10.1.0 | Image processing |
| numpy | 1.24.3 | Numerical computing |
| librosa | 0.10.0 | Audio analysis |

## Configuration

### Environment Variables

Optionally create a `.env` file:

```
MICROPHONE_INDEX=0
CAMERA_INDEX=0
DISPLAY_DURATION=1.5
```

## Known Limitations

1. **Sign Language**: Currently displays individual letter signs. Full word signs and phrases would require a larger dataset.
2. **Gesture Recognition**: Limited to finger counting (0-5 fingers). Complex hand shapes require more training data.
3. **API Dependency**: STT requires Google API access and internet connection.
4. **Performance**: Real-time gesture recognition may be slower on older hardware.

## Future Improvements

- [ ] Add support for common sign language words/phrases
- [ ] Implement more complex gesture recognition using deep learning
- [ ] Add support for offline speech-to-text
- [ ] Create mobile app version
- [ ] Add emotion recognition from video
- [ ] Implement lip-reading capabilities
- [ ] Support for multiple languages
- [ ] Database of pre-recorded sign videos for phrases

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review existing issues for solutions

## Acknowledgments

- Google Cloud Text-to-Speech API
- Google Cloud Speech-to-Text API
- MediaPipe for hand detection
- OpenCV community
- All contributors and testers

## Disclaimer

This project is designed to assist communication but should not be considered a replacement for professional interpretation services for critical communications.
