import os
import re
import subprocess
import threading

from .input_output import send_notification, speak_or_print, start_process
def is_command_safe(cmd):
    unsafe_patterns = [
        r'rm\s+-[rRf]',  # Remove command
        r';',  # Command separator
        r'\|',  # Pipe
        r'&',  # Background process
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, cmd):
            return False
    return True

def run_command(user_input):
    # run_cmd = f"sgpt -s '{user_input}'"
    run_cmd = f"sgpt --no-cache --role commandonly '{user_input}'"
    if is_command_safe(run_cmd):
        print(f"Requested command {run_cmd}")
        result = subprocess.run(run_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        start_process(output,shell=True)
        return output
    else:
        print("Unsafe command. Aborting.")
        return None


def term_sgpt(user_input):
    t = threading.Thread(target=run_command, args=(user_input,))
    t.start()

