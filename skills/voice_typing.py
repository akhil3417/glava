from config import (
    NERD_DICTATION_MODEL,
    NERD_DICTATION_SCRIPT,
    NERD_DICTATION_BINARY,
    NERD_DICTATION,
)
from utils.input_output import start_process, send_notification
from utils.services import get_pid, kill_process


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


def kill_nerd_dictation_command():
    global NERD_DICTATION_SCRIPT
    pid = get_pid(NERD_DICTATION_SCRIPT)
    pid_str = pid.decode(
        "utf-8"
    ).strip()  # Convert bytes to string and remove any whitespace
    pids = pid_str.split("\n")
    for pid in pids:
        kill_process(pid)
    print(f"Killed Nerd Dictation Process with Pid {pids}")
    send_notification(
        f"Voice Dictation Stopped", f"Killed Nerd Dictation Process with Pid {pids}"
    )


def toggle_nerd_dictation_command():
    global NERD_DICTATION
    if NERD_DICTATION:
        NERD_DICTATION = False
        kill_nerd_dictation_command()
    else:
        NERD_DICTATION = True
        start_nerd_dictation_command(
            nerd_dictation_command
        )  # Start the Nerd Dictation.
