import subprocess, os
from config import (
    PIPER_HTTP_SERVER_SCRIPT,
    VOSK_WEBSOCKET_SCRIPT,
    VOSK_MODELS_DIR,
    VOSK_MODEL,
    VOSK_WEBSOCKET_SCRIPT,
)


def start_piper_tts_service(voice_model):
    """
    Start Piper TTS service.
    """
    command = f"python3 {PIPER_HTTP_SERVER_SCRIPT} --sentence_silence 0.2 --noise_scale 0.333 --noise_w 0.333 --length_scale 1.3 -m {voice_model}"
    print(
        f"Starting Piper Http Server on Port 5000 with Default '{os.path.basename(voice_model)}' voice model"
    )
    subprocess.Popen(
        command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


# def get_pid(name):
#     """
#     This function takes a process name as input and returns the process ID (PID) of the given process name.
#     """
#     return subprocess.check_output(["pgrep", "-f", name])


def get_pid(name):
    """
    This function takes a process name as input and returns the process ID (PID) of the given process name.
    """
    try:
        pid = subprocess.check_output(["pgrep", "-f", name])
        return pid.decode(
            "utf-8"
        ).strip()  # Convert bytes to string and remove any whitespace
    except subprocess.CalledProcessError:
        return None


def kill_process(pid):
    """
    Kills the process with the given process ID using the `kill` command.

    Parameters:
    pid (int): The process ID of the process to be killed.

    Returns:
    None
    """
    os.system(f"kill -9 {pid}")


def kill_piper():
    """
    Kills the Piper HTTP server by obtaining its PID, converting it to a string, splitting it by newline,
    and then killing each process. Finally, it prints the PIDs of the killed Piper HTTP server.
    """
    global PIPER_HTTP_SERVER_SCRIPT
    pid = get_pid(PIPER_HTTP_SERVER_SCRIPT)
    if pid is None:  # check if the process was found
        print("Piper HTTP server is not running.")
        return
    pids = pid.split("\n")  # split by newline
    for pid in pids:
        kill_process(int(pid))  # convert PID to integer before killing
    print(f"Killed Piper Http Server with Pids {pids}")


def kill_vosk():
    """
    Kills the Vosk Websocket Server process by getting its PID, converting it to string,
    splitting it into individual PIDs, and then killing each process. Prints the PIDs
    of the killed processes.
    """
    global VOSK_WEBSOCKET_SCRIPT
    pid = get_pid(VOSK_WEBSOCKET_SCRIPT)
    if pid is None:  # check if the process was found
        print("Vosk server is not running.")
        return
    pids = pid.split("\n")  # split by newline
    for pid in pids:
        kill_process(pid)
    print(f"Killed Vosk Websocket Server with Pids {pids}")


def start_vosk_service_command():
    """
    Function to start the Vosk service command.

    This function constructs a command to start the Vosk Websocket Server and then uses subprocess.Popen to execute the command in the shell.

    Parameters:
    None

    Return:
    None
    """
    command = f"python3 {VOSK_WEBSOCKET_SCRIPT} -m {VOSK_MODELS_DIR}{VOSK_MODEL}/"
    print(f"Starting Vosk Websocket Server on Port 2700 with Default model")
    subprocess.Popen(
        command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


def is_aplay_running():
    """
    Check if the 'aplay' process is running and return True if it is, False otherwise.
    """
    try:
        pid = get_pid("aplay")
        return pid != b""
    except subprocess.CalledProcessError:
        return False


def kill_aplay_processes():
    """
    Kill aplay processes by getting their PIDs and killing each process.
    """
    try:
        pid = get_pid("aplay")
        if pid is None:  # check if the process was found
            return
        pids = pid.split("\n")  # split by newline
        for pid in pids:
            kill_process(int(pid))
    except subprocess.CalledProcessError:
        pass
