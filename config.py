import logging
import os
import configparser

# Configure logging
logging.basicConfig(level=logging.INFO)


# Function to get config
def get_config():
    """
    Function to get the configuration from the config.ini file.
    Returns:
        configparser.ConfigParser: The configuration object.
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


config = get_config()


# User specific details
USER = config["USER"]["name"]
HOSTNAME = config["USER"]["hostname"]
EMAIL = config["USER"]["email"]
PASSWORD = config["USER"]["password"]
WAKEWORD = config["USER"]["wakeword"]

# API keys
NEWS_API_KEY = config["API_KEYS"]["news_api_key"]
OPENWEATHER_APP_ID = config["API_KEYS"]["openweather_app_id"]
WOLFRAMALPHA_API = config["API_KEYS"]["wolframalpha_api"]


# services
IS_LISTENING = config["SERVICES"].getboolean("is_listening")
SCREEN_PRINT = config["SERVICES"].getboolean("screen_print")
VOICE = config["SERVICES"].getboolean("voice")
PIPER_HTTP_SERVER = config["SERVICES"].getboolean("piper_http_server")
VOSK_WEBSOCKET_SERVER = config["SERVICES"].getboolean("vosk_websocket_server")
IS_RANDOM_VOICE = config["SERVICES"].getboolean("is_random_voice")

# Other settings
NEWS_HEADLINES_NUMBER = int(config["OTHER_SETTINGS"]["news_headlines_number"])
CITY = config["OTHER_SETTINGS"]["city"]
COUNTRY = config["OTHER_SETTINGS"]["country"]
SHOW_CHAT_HISTORY = config["OTHER_SETTINGS"].getboolean("chat_history")

# browser specific
BROWSER = config["Browser"]["browser"]
PROFILE = config["Browser"]["profile"]


# Directories
BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)  # This will get the directory of the current python file

VOICE_MODELS_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "extensions/piper/models/")
)  # Ensure it's an absolute path


# Voice models
VOICE_MODELS = {
    "1": os.path.join(VOICE_MODELS_DIR, "en_US-libritts-high.onnx"),
    "2": os.path.join(VOICE_MODELS_DIR, "en_US-libritts_r-medium.onnx"),
    "3": os.path.join(VOICE_MODELS_DIR, "en_US-hfc_female-medium.onnx"),
    "4": os.path.join(VOICE_MODELS_DIR, "en_US-amy-medium.onnx"),
    "5": os.path.join(VOICE_MODELS_DIR, "en_US-joe-medium.onnx"),
    "6": os.path.join(VOICE_MODELS_DIR, "en_US-arctic-medium.onnx"),
}

# Speaker IDs
SPEAKER_IDS = {
    "en_US-arctic-medium.onnx": [0, 5, 3, 8, 9, 13, 16, 17],
    "en_US-libritts-high.onnx": list(range(0, 903)),
    "en_US-libritts_r-medium.onnx": list(range(0, 903)),
}

# Voice model and Piper executable
voice_model = VOICE_MODELS.get("3")
PIPER_EXECUTABLE = os.path.join(
    os.path.abspath(os.path.join(BASE_DIR, "extensions/piper/")), "piper"
)

# websocket scripts
PIPER_HTTP_SERVER_SCRIPT = os.path.abspath(
    os.path.join(BASE_DIR, "scripts/piper_websocket_server.py")
)
VOSK_MODELS_DIR = os.path.join(BASE_DIR, "extensions/vosk/")
VOSK_WEBSOCKET_SCRIPT = os.path.join(BASE_DIR, "scripts/vosk_rest_websocket.py")
VOSK_MODEL = "vosk-model-small-en-us-0.15"


# script arguments
PIPER_SCRIPT_ARGS = f"--sentence_silence 0.2 --noise_scale 0.333 --noise_w 0.333 --length_scale 1.3 -m {voice_model}"


STARTUP_MESSAGES = [
    "Cool, Im on it sir.",
    "Okay sir, Im working on it.",
    "Just a second sir.",
]


# Function to get SGPT arguments
def get_sgpt_args():
    """
    Return the command line arguments for running the SGPT model.
    """
    return "--top-p '0.01' --temperature '0.32' --no-cache --chat jarvis"


# Function to get Jarvis prompt
def get_jarvis_prompt():
    return "answer in less than 80 words , be consise ,clear , informative and dont point out spelling mistaks from the user: "
    """
    Return the prompt for JARVIS.
    """
    # return "provide concise ,clear info , focusing only on the necessary information and not including any unnecessary information such as greetings or spelling mistakes from the user: "


# countries=["ae","ar","at","au","be","bg","br","ca","ch","cn","co","cu","cz","de","eg","fr","gb","gr","hk","hu","id","ie","il","in","it","jp","kr","lt","lv","ma","mx","my","ng","nl","no","nz","ph","pl","pt","ro","rs","ru","sa","se","sg","si","sk","th","tr","tw","ua","us","ve","za"]
SITES = {
    "def_search_engine": "https://lite.duckduckgo.com/lite/?q={user_input}&kf=-1&kz=-1&kq=-1&kv=-1&k1=-1&kp=-2&kaf=1&kd=-1",
    "youtube": "http://www.youtube.com/results?aq=f&oq=&search_query={user_input}",
    "invidious": "https://invidious.garudalinux.org/search?q={user_input}",
    "github": "https://github.com/search?ref=simplesearch&q={user_input}",
    "google_map": "https://www.google.com/maps/search/{user_input}/",
    "wikipedia": "http://www.wikipedia.org/search-redirect.php?language=en&go=Go&search={user_input}",
    "reddit": "https://www.reddit.com/search/?q={user_input}",
    "amazon": "https://www.amazon.in/s?k={user_input}",
    "stackoverflow": "https://stackoverflow.com/search?q={user_input}",
    "google": "http://www.google.com/search?hl=en&ie=utf-8&oe=utf-8&q={user_input}",
}
