#!/usr/bin/env python3
import argparse
import asyncio
import os
import socket

import typer
from pynput import keyboard
from rich.console import Console

# Import necessary modules
from config import (
    HOSTNAME,
    IS_LISTENING,
    PIPER_HTTP_SERVER,
    USER,
    VOICE,
    VOICE_MODELS,
    SHOW_CHAT_HISTORY,
    voice_model,
)
from skills.browser import (
    open_browser_command,
    open_websites,
    query_web_command_async,
    web_search,
)
from skills.info import (
    calculate_wolframe,
    movie_command,
    what_is_wolframe,
    wikipedia_command_async,
)
from skills.linux import ip_address_command_async
from skills.music import stream_yt
from skills.news import google_news_command, read_news
from skills.weather import weather_report_command

# from skills.music import play_song, run_stream_command_async
from utils.command_handlers import sgpt_shell_ai, term_sgpt
from utils.input_output import (
    change_voice_model_command,
    generate_response,
    get_transcript,
    start_listening,
    toggle_is_listening_command,
    toggle_piper_http_server_command,
    toggle_random_voice_command,
    toggle_voice_command,
    toggle_vosk_websocket_server_command,
)
from utils.services import start_piper_tts_service, start_vosk_service_command
from utils.shellgpt_check import shellgpt_check
from utils.chat_history import show_chat_history
from utils.greetings import greet_user
from skills.image_generator import generate_image

from skills.voice_typing import (
    toggle_nerd_dictation_command,
    start_nerd_dictation_command,
    kill_nerd_dictation_command,
)
from utils.memory_consumption import tell_memory_consumption


# Parse command-line arguments
parser = argparse.ArgumentParser(description="Interactive SGPT.")
parser.add_argument("--model", type=str, default="2", help="Voice model to use")
args = parser.parse_args()

# Get voice model from command-line arguments
VOICE_MODEL = VOICE_MODELS[args.model]

console = Console()


def ensure_piper_model(voice_model):
    """
    Ensure the existence of a voice model file.

    Parameters:
    voice_model (str): The path to the voice model file.

    Returns:
    bool: True if the voice model file exists, otherwise False.
    """
    if not os.path.exists(voice_model):
        print(f"Voice model file not found at {voice_model}")
        return False
    return True


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


async def handle_command(user_input):
    """
    Handle user input and execute the corresponding command , based on key(user_input) and value(command) pair.

    Args:
    user_input (str): The user input to be processed.
    """
    commands = {
        # terminal
        #
        "jarvis": sgpt_shell_ai,
        "terminal": term_sgpt,
        "term": term_sgpt,
        # browser
        #
        # "test": open_websites,  #  FIXME 2024-03-03: not very good and maybe not worth improving , sgpt_shell_ai might be possible replacement
        "open browser": open_browser_command,
        "search": web_search,
        "query for": query_web_command_async,
        # info
        #
        "google news": google_news_command,
        "get news": read_news,
        "wikipedia": wikipedia_command_async,
        # weather
        #
        "weather": weather_report_command,
        # wolframalpha
        #
        "calculate": calculate_wolframe,
        "alpha": what_is_wolframe,
        # linux
        #
        "ip address": ip_address_command_async,
        # aud & vid
        #
        "generate image": generate_image,
        "create image": generate_image,
        "play": stream_yt,
        "movie": movie_command,
        # "send an email": send_email_command,
        #
        # assistant controls
        "modelv": change_voice_model_command,
        "vcc": toggle_voice_command,
        "tll": toggle_is_listening_command,
        "rvt": toggle_random_voice_command,
        "pipt": toggle_piper_http_server_command,
        "votss": toggle_vosk_websocket_server_command,
        "toggle dictation": toggle_nerd_dictation_command,
        "start dictation": toggle_nerd_dictation_command,
        "start writing": start_nerd_dictation_command,
        "stop writing": kill_nerd_dictation_command,
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
                    # run the function in a separate thread
                    loop = asyncio.get_event_loop()
                    task = loop.run_in_executor(None, func, user_input)
                    await task
                    # func(user_input)
                    return
            except Exception as e:
                raise CommandHandlingError(f"An error occurred in {func.__name__}:", e)

    generate_response(user_input)


def is_port_open(host, port):
    """
    Check if a given host and port combination is open for communication.

    Args:
        host (str): The host to check for open port.
        port (int): The port number to check for availability.

    Returns:
        bool: True if the port is open, False otherwise.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


async def voice_sgpt(IS_LISTENING):
    """
    Asynchronous function for voice recognition using Vosk.
    It takes a boolean parameter IS_LISTENING.
    """
    start_vosk_service_command()
    while not is_port_open("localhost", 2700):
        await asyncio.sleep(1)
    print("Listening")
    while True:
        IS_LISTENING = True
        try:
            listen_task = await start_listening("ws://localhost:2700", IS_LISTENING)
            await listen_task
            user_input = get_transcript()
            if "stop listening" in get_transcript():
                break
            await handle_command(user_input)
        except Exception as e:
            raise VoiceInputError("An error occurred in voice_sgpt:", e)


async def handle_async_function(func, *args):
    """
    An asynchronous function that handles the execution of the input function with the provided arguments.
    It catches any exceptions raised during the execution and raises a CommandHandlingError with an appropriate message.

    Parameters:
    - func: The function to be executed asynchronously.
    - *args: The arguments to be passed to the function.

    Returns:
    This function does not return anything directly, but it may raise a CommandHandlingError if an exception occurs during the execution of the input function.
    """
    try:
        await func(*args)
    except Exception as e:
        raise CommandHandlingError(f"An error occurred in {func.__name__}:", e)


# run checks

if VOICE:
    if not ensure_piper_model(voice_model):
        console.print(f"The voice model file is missing.", style="red")
        raise SystemExit
# checks
shellgpt_check()

# start piper
if PIPER_HTTP_SERVER:
    start_piper_tts_service(voice_model)


async def interactive_sgpt():
    if SHOW_CHAT_HISTORY:
        show_chat_history("jarvis")  # print the chat history when the program starts
    greet_user(USER, HOSTNAME)
    while True:
        user_input = typer.prompt(">>>", prompt_suffix=" ").replace(
            "'", ""
        )  # remove upperquotes
        if user_input.lower() == "exit":
            break
        if user_input.lower() == "clear":
            os.system("clear")  # clear the console
        elif user_input.lower() == "v":
            # handle voice input with voice_sgpt
            try:
                await handle_async_function(voice_sgpt, IS_LISTENING)
                # await voice_sgpt(IS_LISTENING)
            except CommandHandlingError as e:
                console.print(f"An error occurred: {e}", style="red")
        else:
            # handle user command
            try:
                await handle_async_function(handle_command, user_input)
                # await handle_command(user_input)
            except CommandHandlingError as e:
                console.print(f"An error occurred: {e}", style="red")


if __name__ == "__main__":
    asyncio.run(interactive_sgpt())
