import asyncio
import logging
import os
import random
import subprocess
import threading

from config import (
    IS_LISTENING,
    IS_RANDOM_VOICE,
    PIPER_EXECUTABLE,
    PIPER_HTTP_SERVER,
    SCREEN_PRINT,
    SPEAKER_IDS,
)
from config import VOICE as global_voice  # STARTUP_MESSAGES,
from config import (
    VOICE_MODELS,
    VOSK_WEBSOCKET_SERVER,
    get_jarvis_prompt,
    get_sgpt_args,
    voice_model,
)

from .services import (
    kill_piper,
    kill_vosk,
    start_piper_tts_service,
    kill_aplay_processes,
    is_aplay_running,
)
from .speech_recognition import start_listening


def toggle_is_listening_command():
    """
    Toggles the IS_LISTENING global variable and prints its status.
    """
    global IS_LISTENING
    IS_LISTENING = not IS_LISTENING
    print(f"Is Listening status: {IS_LISTENING}")


def toggle_random_voice_command():
    """
    Toggles the global variable IS_RANDOM_VOICE to its opposite value and prints the new status.
    """
    global IS_RANDOM_VOICE
    IS_RANDOM_VOICE = not IS_RANDOM_VOICE
    print(f"Random voice status: {IS_RANDOM_VOICE}")


def toggle_voice_command():
    """
    Toggles the global_voice variable to its opposite value and prints the updated voice status.
    """
    global global_voice
    global_voice = not global_voice
    print(f"Voice status: {global_voice}")


def speaker_ids(voice_model):
    """
    Function to retrieve speaker ids based on the provided voice model.

    Args:
    voice_model (str): The voice model for which speaker ids are to be retrieved.

    Returns:
    str or None: Randomly selected speaker ids if the voice model is found in the SPEAKER_IDS dictionary, otherwise None.
    """
    voice_model = os.path.basename(
        voice_model
    )  # Strip the path from the voice_model value
    if voice_model in SPEAKER_IDS:
        return random.choice(SPEAKER_IDS[voice_model])
    else:
        return None


def get_audio_stream(json_input=False):
    """
    Function to get the audio stream with optional JSON input.
    """
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
    """
    A function to either speak or print the given text based on the specified parameters.

    Args:
        text (str): The text to be spoken or printed.
        VOICE (str, optional): The voice to be used for speaking. Defaults to None.
        json_input (bool, optional): Flag indicating whether the input is in JSON format. Defaults to False.

    Returns:
        None
    """
    if PIPER_HTTP_SERVER:
        command = f"curl -G --data-urlencode 'text={text}' 'localhost:5000' 2>/dev/null| aplay -r 22050 -f S16_LE -t raw - 2>/dev/null"
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


def speak(text, json_input=False):
    """
    A function that speaks the given text using audio stream, with an option to provide input as JSON.
    Parameters:
        text (str): The text to be spoken.
        json_input (bool, optional): Flag to indicate if the input is in JSON format. Defaults to False.
    """
    command = get_audio_stream(json_input)
    try:
        subprocess.run(command, shell=True, check=True, input=text, text=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {command}. Error: {e}")


def get_transcript():
    """
    Function to retrieve the content of the transcript file.
    """
    try:
        with open("/tmp/transcript.txt", "r") as f:
            return f.read().replace("'", "")
    except FileNotFoundError:
        logging.error("Transcript file not found")
        return ""


async def ask_for_input(user_input):
    """
    Asynchronous function to ask for user input, start listening in the background, and return the user input.

    Parameters:
    user_input: str - The user input to be processed.

    Returns:
    str - The user input after processing.
    """
    # Run listen function in the background
    global listen_task
    listen_task = await start_listening("ws://localhost:2700", True)
    # Wait for listen task to complete
    await listen_task
    # Get user input
    user_input = get_transcript()
    return user_input


def generate_response(user_input):
    """
    Function to generate a response based on user input.

    Args:
        user_input: The input provided by the user.

    Returns:
        None
    """
    # speak_or_print(random.choice(STARTUP_MESSAGES))
    # Kill all 'aplay' processes
    if is_aplay_running():
        kill_aplay_processes()  # in case another request is made , to avoid two audios streaming
    command = get_command(user_input)
    start_process(command, shell=True)
    # run_shell_command_and_return_output(command, shell=True)
    # subprocess.run(command, shell=True)


# def generate_response(user_input):
#     try:
#         kill_aplay_processes()  # in case another request is make , to avoid two audios streaming
#         command = get_command(user_input)
#         t = threading.Thread(target=start_process, args=(command, True))
#         t.start()
#     except Exception as e:
#         print("An error occurred in handle_command:", e)


def start_process(
    cmd, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
):
    """
    Function to start a process with the given command and optional parameters.

    Args:
        cmd (str): The command to be executed.
        shell (bool, optional): Whether to use the shell as the program to execute. Defaults to False.
        stdout (file, optional): A file object to redirect the standard output to. Defaults to subprocess.DEVNULL.
        stderr (file, optional): A file object to redirect the standard error to. Defaults to subprocess.STDOUT.

    Returns:
        None
    """
    try:
        subprocess.Popen(cmd, shell=shell, stdout=stdout, stderr=stderr)
        # subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except TypeError:
        pass
    except Exception as e:
        print("An error occurred in handle_command:", e)


def run_shell_command_and_return_output(
    cmd,
    shell=False,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    print_output=False,
):
    """
    Run a shell command and return the output.

    Args:
        cmd (str): The shell command to be executed.
        shell (bool, optional): Whether to use the shell as the program to execute. Defaults to False.
        stdout: Where to redirect the standard output. Defaults to subprocess.PIPE.
        stderr: Where to redirect the standard error. Defaults to subprocess.STDOUT.
        print_output (bool, optional): Whether to print the output. Defaults to False.

    Returns:
        None: If an error occurs.
        tuple: The exit code and output if print_output is False.
    """
    try:
        process = subprocess.Popen(
            cmd,
            shell=shell,
            stdout=stdout,
            stderr=stderr,
        )
        output, _ = process.communicate()
        # exit_code = process.returncode
        if print_output:
            # return print(f"Exit code: {exit_code}, Output:\n{output.decode()}")
            # return print(f"Output:\n{output.decode()}")
            return print(f"\n{output.decode()}")
        # return exit_code, output
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output.decode()
    except Exception as e:
        return None, f"An error occurred: {str(e)}"


async def input_without_listen(user_input):
    """
    Asynchronous function to get user input without blocking the event loop.

    Args:
        user_input: The input prompt for the user.

    Returns:
        The user input provided by the user.
    """
    user_input = await asyncio.to_thread(input, "Enter Query:")
    #     user_input = input("Enter:")
    return user_input


async def input_with_listen(user_input):
    """
    Asynchronously prompts the user for input while displaying the message "Listening:".
    Returns the user input provided.
    """
    user_input = await ask_for_input("Listening:")
    return user_input


async def take_command():
    """
    Asynchronously takes a command from the user.
    """
    user_input = None
    #     if IS_LISTENING is None:
    #         IS_LISTENING = global_listening
    if IS_LISTENING:
        user_input = await input_with_listen("Listening:")
    else:
        user_input = await input_without_listen("Enter: ")
    return user_input


def send_notification(title, message):
    """
    Send a notification using notify-send
    """
    # Send a notification using notify-send
    start_process(["notify-send", title, message])


def change_voice_model_command():
    """
    A function to change the voice model command. It prints the available voice models, takes user input for the model choice, and updates the global voice model variable if the chosen model is valid. It also handles the restarting of the Piper TTS server with the new voice model if applicable. Returns the updated voice model or prints an error message for an invalid choice.
    """
    global voice_model  # Declare that the voice_model variable will be used globally
    print("Choose voice model:")
    for choice, model in VOICE_MODELS.items():
        print(f"{choice}: {os.path.splitext(os.path.basename(model))[0]}")
    model_choice = input("Enter your choice: ")
    if model_choice in VOICE_MODELS:
        if (
            voice_model != VOICE_MODELS[model_choice]
        ):  # Check if the voice model has changed
            voice_model = VOICE_MODELS[model_choice]
            if PIPER_HTTP_SERVER:
                print(
                    f"Killing and Restarting Piper Tts server with {voice_model} model."
                )
                kill_piper()
                start_piper_tts_service(
                    voice_model
                )  # Start the service with the new voice model
            return voice_model
    else:
        print("Invalid choice. Please choose a number from the list.")

def get_command(user_input):
    """
    A function to generate a command based on user input, with various conditional branches for different scenarios.
    """
    sgpt_args = get_sgpt_args()
    jarvis_user_input = get_jarvis_prompt()

    if PIPER_HTTP_SERVER:
        command = f"sgpt {sgpt_args} '{jarvis_user_input} {user_input}'| tee /dev/tty"
        if global_voice and SCREEN_PRINT:
            sgpt_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output = sgpt_process.communicate()[0].decode().strip().replace("'", "")
            curl_command = f"curl -G --data-urlencode 'text={output}' 'localhost:5000' 2>/dev/null| aplay -r 22050 -f S16_LE -t raw - 2>/dev/null"
            start_process(curl_command, shell=True)
            return
        elif global_voice and not SCREEN_PRINT:
            command = command.split("|")[0]
            sgpt_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output = sgpt_process.communicate()[0].decode().strip().replace("'", "")
            curl_command = f"curl -G --data-urlencode 'text={output}' 'localhost:5000' 2>/dev/null| aplay -r 22050 -f S16_LE -t raw - 2>/dev/null"
            start_process(curl_command, shell=True)
            return
        else:
            start_process(command, shell=True)
    else:
        if global_voice and SCREEN_PRINT:
            audio_stream = get_audio_stream()
            return f"sgpt {sgpt_args} '{jarvis_user_input} {user_input}' | tee /dev/tty |{audio_stream} "
        elif global_voice and not SCREEN_PRINT:
            audio_stream = get_audio_stream()
            return (
                f"sgpt {sgpt_args} '{jarvis_user_input} {user_input}' | {audio_stream} "
            )
        else:
            return f"sgpt {sgpt_args} '{jarvis_user_input} {user_input}'"


def toggle_piper_http_server_command():
    """
    Function to toggle the Piper HTTP server command.
    This function toggles the global variable PIPER_HTTP_SERVER, and depending on its value, either kills the Piper or starts the Piper TTS service.
    """
    global PIPER_HTTP_SERVER
    if PIPER_HTTP_SERVER:
        PIPER_HTTP_SERVER = False
        kill_piper()
    else:
        PIPER_HTTP_SERVER = True
        start_piper_tts_service()  # Start the PIPER_HTTP_SERVER


def toggle_vosk_websocket_server_command():
    """
    Toggles the Vosk websocket server command.
    """
    global VOSK_WEBSOCKET_SERVER
    if VOSK_WEBSOCKET_SERVER:
        VOSK_WEBSOCKET_SERVER = False
        kill_vosk()
    else:
        VOSK_WEBSOCKET_SERVER = True
        start_piper_tts_service()  # Start the VOSK_WEBSOCKET_SERVER
