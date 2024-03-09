from config import (
    NERD_DICTATION_MODEL,
    NERD_DICTATION_SCRIPT,
    NERD_DICTATION_BINARY,
    IS_VOICE_DICTATION,
)
from utils.input_output import start_process, send_notification
from utils.services import get_pid


def start_nerd_dictation_command():
    # Define the command
    nerd_dictation_command = [
        NERD_DICTATION_BINARY,
        "begin",
        "--vosk-model-dir={}".format(NERD_DICTATION_MODEL),
        "--numbers-as-digits",
        "--numbers-use-separator",
        "--numbers-min-value=10",
        "--numbers-no-suffix",
        "--punctuate-from-previous-timeout=0.5",
        "--full-sentence",
        "--config={}".format(NERD_DICTATION_SCRIPT),
    ]
    start_process(nerd_dictation_command)
    send_notification(
        "Voice Dictation Started",
        "Say 'Start Writing' or 'Stop writing' to start/stop Dictation",
    )


def resume_nerd_dictation_command():
    start_process([NERD_DICTATION_BINARY, "resume"])
    send_notification("Voice Dictation Resumed", "")


def suspend_nerd_dictation_command():
    start_process([NERD_DICTATION_BINARY, "suspend"])
    send_notification("Voice Dictation Suspended", "")


def init_nerd_dictation_command():
    if IS_VOICE_DICTATION:
        start_nerd_dictation_command()
        suspend_nerd_dictation_command()


def kill_nerd_dictation_command():
    start_process([NERD_DICTATION_BINARY, "end"])
    send_notification("Voice Dictation Killed", "")


def manage_nerd_dictation_command():
    pid = get_pid(NERD_DICTATION_BINARY)

    if pid and pid.isdigit():  # Check if PID is a valid number
        resume_nerd_dictation_command()
    else:
        start_nerd_dictation_command()
