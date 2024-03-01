import os
import re
import subprocess
import threading

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

