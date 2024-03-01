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

SPEAKER_IDS = {
    'en_US-arctic-medium.onnx': [0, 5, 3, 8, 9, 13, 16, 17],
    'en_US-libritts-high.onnx': list(range(0, 903)),
    'en_US-libritts_r-medium.onnx': list(range(0, 903)),
}

PIPER_EXECUTABLE = os.path.join(os.path.abspath(os.path.join(BASE_DIR, 'extensions/piper/')), 'piper')
PIPER_HTTP_SERVER=False
PIPER_HTTP_SERVER_SCRIPT=os.path.abspath(os.path.join(BASE_DIR, 'scripts/piper_websocket_server.py'))
PIPER_SCRIPT_ARGS = f"--sentence_silence 0.2 --noise_scale 0.333 --noise_w 0.333 --length_scale 1.3 -m {voice_model}"

VOSK_WEBSOCKET_SERVER=False
VOSK_WEBSOCKET_SCRIPT=os.path.join(BASE_DIR,'scripts/vosk_rest_websocket.py')
VOSK_MODELS_DIR=os.path.join(BASE_DIR,'extensions/vosk/')
VOSK_MODEL="vosk-model-en-in-0.5"
# BROWSER = "qutebrowser"
# PROFILE = ""
BROWSER = "firefox"
PROFILE = "-p KodachiBrowserLight"
TERMINAL="st"

STARTUP_MESSAGES = [
    "Cool, Im on it sir.",
    "Okay sir, Im working on it.",
    "Just a second sir.",
]

# countries=["ae","ar","at","au","be","bg","br","ca","ch","cn","co","cu","cz","de","eg","fr","gb","gr","hk","hu","id","ie","il","in","it","jp","kr","lt","lv","ma","mx","my","ng","nl","no","nz","ph","pl","pt","ro","rs","ru","sa","se","sg","si","sk","th","tr","tw","ua","us","ve","za"]
COUNTRY="in"
