import subprocess,os
from config import PIPER_HTTP_SERVER_SCRIPT,voice_model,VOSK_WEBSOCKET_SCRIPT,VOSK_MODELS_DIR,VOSK_MODEL,VOSK_WEBSOCKET_SCRIPT

def start_piper_tts_service():
    command = f"python3 {PIPER_HTTP_SERVER_SCRIPT} --sentence_silence 0.2 --noise_scale 0.333 --noise_w 0.333 --length_scale 1.3 -m {voice_model}"
    print(f"Starting Piper Http Server on Port 5000 with Default {os.path.basename(voice_model)} model")
    # start_process(command,shell=True)
    subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
def get_pid(name):
    return subprocess.check_output(["pgrep", "-f", name])

def kill_process(pid):
    os.system(f'kill -9 {pid}')

def kill_piper():
    global PIPER_HTTP_SERVER_SCRIPT
    pid=get_pid(PIPER_HTTP_SERVER_SCRIPT)
    pid_str = pid.decode('utf-8').strip()  # Convert bytes to string and remove any whitespace
    pids = pid_str.split('\n')
    for pid in pids:
        kill_process(pid)
    print(f"Killed Piper Http Server with Pids {pids}")
