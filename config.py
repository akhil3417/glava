import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

USER = 'Charlie'
HOSTNAME = 'Jarvis'
EMAIL = ""
PASSWORD = ""
NEWS_API_KEY = ""
OPENWEATHER_APP_ID = ""
NEWS_HEADLINES_NUMBER=10


BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # This will get the directory of the current python file
VOICE_MODELS_DIR = os.path.abspath(os.path.join(BASE_DIR,'extensions/piper/models/'))  # Ensure it's an absolute path
VOICE_MODELS = {
    '1': os.path.join(VOICE_MODELS_DIR, 'en_US-libritts-high.onnx'),
    '2': os.path.join(VOICE_MODELS_DIR, 'en_US-libritts_r-medium.onnx'),
    '3': os.path.join(VOICE_MODELS_DIR, 'en_US-hfc_female-medium.onnx'),
    '4': os.path.join(VOICE_MODELS_DIR, 'en_US-amy-medium.onnx'),
    '5': os.path.join(VOICE_MODELS_DIR, 'en_US-joe-medium.onnx'),
    '6': os.path.join(VOICE_MODELS_DIR, 'en_US-arctic-medium.onnx'),

}

