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

def toggle_is_listening_command():
    global IS_LISTENING
    IS_LISTENING = not IS_LISTENING
    print(f"Is Listening status: {IS_LISTENING}")

def speaker_ids(voice_model):
    voice_model = os.path.basename(voice_model)  # Strip the path from the voice_model value
    if voice_model in SPEAKER_IDS:
        return random.choice(SPEAKER_IDS[voice_model])
    else:
        return None

def get_audio_stream(json_input=False):
    global voice_model
    command = f"{PIPER_EXECUTABLE} --model {voice_model}"
    if IS_RANDOM_VOICE:
       speaker_id = speaker_ids(voice_model)
       if speaker_id is not None:
           command += f" --speaker {speaker_id}"
           print(speaker_id)
    if json_input:
        command += " --json-input"
    command += " --sentence_silence 0.2 --noise_scale 0.333 --noise_w 0.333 --length_scale 1.3  --output-raw 2>/dev/null |  aplay -r 22050 -f S16_LE -t raw - 2>/dev/null "
    return command

def speak_or_print(text, VOICE=None, json_input=False):
    if PIPER_HTTP_SERVER:
       command = f"curl -G --data-urlencode 'text={text}' 'localhost:5000' | aplay -r 22050 -f S16_LE -t raw - 2>/dev/null"
       subprocess.run(command, shell=True, check=True, input=text, text=True)
       return
    elif VOICE is not None:
        VOICE = global_voice
        command = get_audio_stream(json_input)
        try:
            subprocess.run(command, shell=True, check=True, input=text, text=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running command: {command}. Error: {e}")
            pass
    else:
        print(text)
def toggle_piper_http_server_command():
    global PIPER_HTTP_SERVER
    if PIPER_HTTP_SERVER:
        PIPER_HTTP_SERVER = False
        kill_piper()
    else:
        PIPER_HTTP_SERVER = True
        start_piper_tts_service()  # Start the PIPER_HTTP_SERVER

def toggle_vosk_websocket_server_command():
    global VOSK_WEBSOCKET_SERVER
    if VOSK_WEBSOCKET_SERVER:
        VOSK_WEBSOCKET_SERVER = False
        kill_vosk()
    else:
        VOSK_WEBSOCKET_SERVER = True
        start_piper_tts_service()  # Start the VOSK_WEBSOCKET_SERVER
