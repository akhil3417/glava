#!/usr/bin/env python3
import argparse
import asyncio
import os
from datetime import datetime

from pynput import keyboard

# from config import VOICE_MODELS , USER , HOSTNAME
# Import necessary modules
from config import HOSTNAME, IS_LISTENING, USER, VOICE_MODELS, PIPER_HTTP_SERVER
from skills.browser import (
    open_browser_command,
    open_websites,
    open_youtube_browser_command_async,
    query_web_command_async,
    web_search,
)
from skills.info import (
    calculate_command,
    google_news_command,
    movie_command,
    read_news,
    weather_command,
    what_is_wolframe,
    wikipedia_command_async,
    weather_forecast,
)
from skills.linux import ip_address_command_async, open_new_shell_command
from skills.music import play_song, run_stream_async
from utils.command_handlers import term_sgpt
from utils.services import start_vosk_service_command, start_piper_tts_service
from utils.memory_consumption import tell_memory_consumption
from utils.input_output import (
    generate_response,
    get_transcript,
    speak_or_print,
    start_listening,
    toggle_is_listening_command,
    toggle_random_voice_command,
    toggle_voice_command,
    change_voice_model_command,
    toggle_piper_http_server_command,
    toggle_vosk_websocket_server_command,
)

from rich import print as rich_print
from rich.rule import Rule
from rich.prompt import Prompt
import typer


# Parse command-line arguments
parser = argparse.ArgumentParser(description="Interactive SGPT.")
parser.add_argument("--model", type=str, default="2", help="Voice model to use")
args = parser.parse_args()

# Get voice model from command-line arguments
VOICE_MODEL = VOICE_MODELS[args.model]


def ensure_piper_models():
    for voice_model_key, voice_model_path in VOICE_MODELS.items():
        if not os.path.exists(voice_model_path):
            print(f"Voice model file not found at {voice_model_path}")


# ensure_piper_models()


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


def greet_me(USER, HOSTNAME):
    time_of_day = get_time_of_day()
    rich_print(
        f"{time_of_day} [bold magenta]{USER}[/bold magenta]. I am [bold magenta]{HOSTNAME}[/bold magenta]. How may I assist you?"
    )


greet_me(USER, HOSTNAME)

# keyboard_listener = keyboard.GlobalHotKeys({
#     # '<ctrl>+<alt>+k': start_listening,
#     # '<ctrl>+<alt>+p': stop_listening
#     '<ctrl>+b': speech_recognition,
#     '<ctrl>+B': stop_listening
# })
# keyboard_listener.start()


class Error(Exception):
    """Base class for other exceptions"""

    pass


class VoiceInputError(Error):
    """Raised when there's a problem with voice input"""

    pass


class CommandHandlingError(Error):
    """Raised when there's a problem handling a command"""

    pass


if PIPER_HTTP_SERVER:
    start_piper_tts_service()


async def handle_command(user_input):
    commands = {
        "term": term_sgpt,
        # browser
        "open": open_websites,
        "browser": open_browser_command,
        "search for": web_search,
        "query for": query_web_command_async,
        "youtube": open_youtube_browser_command_async,
        # info
        "google news": google_news_command,
        "get news": read_news,
        "wiki": wikipedia_command_async,
        # "weather":weather_command,
        #  FIXME 2024-03-01: choose if use a city var , or extract from user_input
        "weather forecast": weather_forecast,
        "calculate": calculate_command,
        "alpha": what_is_wolframe,
        # linux
        "ip address": ip_address_command_async,
        "new shell": open_new_shell_command,
        # music
        "dream": run_stream_async,
        "play": play_song,
        # "movie": movie_command,
        # "send an email": send_email_command,
        # assistant controls
        "modelv": change_voice_model_command,
        "vcc": toggle_voice_command,
        "tll": toggle_is_listening_command,
        "rvt": toggle_random_voice_command,
        "pipt": toggle_piper_http_server_command,
        "votss": toggle_vosk_websocket_server_command
        #
    }

    for command, func in commands.items():
        if command in user_input:
            user_input = user_input.replace(command, "").strip()
            try:
                if "_command" in func.__name__ and "_async" in func.__name__:
                    await func()
                    return
                if "_command" in func.__name__:
                    func()
                    return
                if "_async" in func.__name__:
                    await func(user_input)
                    return
                else:
                    func(user_input)
                    return
            except Exception as e:
                raise CommandHandlingError(f"An error occurred in {func.__name__}:", e)

    generate_response(user_input)


async def voice_sgpt(IS_LISTENING):
    start_vosk_service_command()
    while True:
        IS_LISTENING = True
        try:
            listen_task = await start_listening("ws://localhost:2700", IS_LISTENING)
            await listen_task
            user_input = get_transcript()
            await handle_command(user_input)
        except Exception as e:
            raise VoiceInputError("An error occurred in voice_sgpt:", e)


async def handle_async_function(func, *args):
    try:
        await func(*args)
    except Exception as e:
        raise CommandHandlingError(f"An error occurred in {func.__name__}:", e)


async def interactive_sgpt():
    while True:
        user_input = typer.prompt(">>>", prompt_suffix=" ")
        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "v":
            print("Listening")
            try:
                await handle_async_function(voice_sgpt, IS_LISTENING)
            except CommandHandlingError as e:
                print(f"An error occurred: {e}")
        else:
            try:
                await handle_async_function(handle_command, user_input)
            except CommandHandlingError as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(interactive_sgpt())
