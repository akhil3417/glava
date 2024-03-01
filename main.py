#!/usr/bin/env python3
import argparse
import asyncio
import os
from datetime import datetime

from pynput import keyboard

# from config import VOICE_MODELS , USER , HOSTNAME
# Import necessary modules
from config import HOSTNAME, IS_LISTENING, USER, VOICE_MODELS, PIPER_HTTP_SERVER
from skills.browser import (open_browser_command, open_websites,
                            open_youtube_browser_command_async,
                            query_web_command_async, web_search)
from skills.info import (calculate_command, google_news_command, movie_command,
                         read_news, weather_command, what_is_wolframe,
                         wikipedia_command_async,weather_forecast)
from skills.linux import ip_address_command_async, open_new_shell_command
from skills.music import play_song, run_stream_async
from utils.command_handlers import term_sgpt
from utils.services import start_vosk_service_command
from utils.memory_consumption import tell_memory_consumption
from utils.input_output import (generate_response, get_transcript,
                                speak_or_print, start_listening,
                                toggle_is_listening_command,
                                toggle_random_voice_command,
                                toggle_voice_command,change_voice_model_command,toggle_piper_http_server_command,toggle_vosk_websocket_server_command)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Interactive SGPT.')
parser.add_argument('--model', type=str, default='2', help='Voice model to use')
args = parser.parse_args()

# Get voice model from command-line arguments
VOICE_MODEL = VOICE_MODELS[args.model]

def ensure_piper_models():
    for voice_model_key, voice_model_path in VOICE_MODELS.items():
        if not os.path.exists(voice_model_path):
            print(f"Voice model file not found at {voice_model_path}")
ensure_piper_models()


def get_time_of_day():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        return "Good morning"
    elif (hour >= 12) and (hour <= 16):
        return "Good afternoon"
    elif (hour >= 16) and (hour < 19):
        return "Good evening"
    else:
        return "Hello"

def greet_me(user, hostname):
    time_of_day = get_time_of_day()
    speak_or_print(f"{time_of_day} {user}. I am {hostname}. How may I assist you?")

async def handle_command(user_input):
    commands = {
        "term": term_sgpt,
#browser
        "open": open_websites,
        "browser": open_browser_command,
        "search for": web_search,
        "query for":query_web_command_async,
        "youtube": open_youtube_browser_command_async,
#info
        "google news":google_news_command,
        "get news":read_news,
        "wiki":wikipedia_command_async,
        # "weather":weather_command,
        #  FIXME 2024-03-01: choose if use a city var , or extract from user_input
        "weather forecast":weather_forecast,
        "calculate": calculate_command,
        "alpha": what_is_wolframe,
#linux
        "ip address": ip_address_command_async,
        "new shell": open_new_shell_command,
#music
        "dream": run_stream_async,
        "play": play_song,
        # "movie": movie_command,
        # "send an email": send_email_command,

#assistant controls
        "modelv": change_voice_model_command,
        "vcc": toggle_voice_command,
        "tll": toggle_is_listening_command,
        "rvt": toggle_random_voice_command,
        "pipt": toggle_piper_http_server_command,
        "voss": start_vosk_service_command,
        "votss": toggle_vosk_websocket_server_command
#
    }

    for command, func in commands.items():
        if command in user_input:
            user_input = user_input.replace(command, "").strip()
            if "_command" in func.__name__ and  "_async" in func.__name__:
                await func()
                return
            if "_command" in func.__name__:
                func()
                return
            if "_async" in func.__name__:
                await func(user_input)
                # asyncio.run(func())
                return
            else:
                func(user_input)
            return

    generate_response(user_input)

async def voice_sgpt(IS_LISTENING):
    while True:
        IS_LISTENING = True
        listen_task = await start_listening('ws://localhost:2700', IS_LISTENING)
        await listen_task
        user_input = get_transcript()
        await handle_command(user_input)


async def interactive_sgpt():
    while True:
        user_input = input(">>\n")
        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 'v':
            print("Listening")
            try:
                await voice_sgpt(IS_LISTENING)
            except Exception as e:
                print("An error occurred in voice_sgpt:", e)
        else:
            try:
                await handle_command(user_input)
            except TypeError:
                pass
            except Exception as e:
                print("An error occurred in handle_command:", e)


if __name__ == "__main__":
    asyncio.run(interactive_sgpt())
