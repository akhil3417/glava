import asyncio
import logging
import os
import random
import shlex
import subprocess
import threading

from config import (IS_LISTENING, IS_RANDOM_VOICE, PIPER_EXECUTABLE,
                    PIPER_HTTP_SERVER, SCREEN_PRINT,VOICE_MODELS ,SPEAKER_IDS,VOICE as global_voice,STARTUP_MESSAGES,VOSK_WEBSOCKET_SERVER)
from config import get_jarvis_prompt, get_sgpt_args,voice_model
from .speech_recognition import start_listening
from .services import kill_vosk, start_piper_tts_service,kill_piper
def speaker_ids(voice_model):
    voice_model = os.path.basename(voice_model)  # Strip the path from the voice_model value
    if voice_model in SPEAKER_IDS:
        return random.choice(SPEAKER_IDS[voice_model])
    else:
        return None

def toggle_piper_http_server_command():
    global PIPER_HTTP_SERVER
    if PIPER_HTTP_SERVER:
        PIPER_HTTP_SERVER = False
        kill_piper()
    else:
        PIPER_HTTP_SERVER = True
        start_piper_tts_service()  # Start the PIPER_HTTP_SERVER
