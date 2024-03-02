import os
import re
import subprocess
import threading

from .input_output import send_notification, speak_or_print, start_process


def is_command_safe(cmd):
    unsafe_patterns = [
        r"rm\s+-[rRf]",  # Remove command
        r";",  # Command separator
        r"\|",  # Pipe
        # r"&",  # Background process
        r"(^|\s)(cat|cd|chmod|chown|cp|df|diff|du|find|fmt|grep|less|ln|ls|make|mkdir|mv|rm|sed|sort|tail|tar|touch|uniq|vi|wc)($|\s)",  # File manipulation commands
        r"(^|\s)(curl|wget|ssh|ftp|ping|telnet)($|\s)",  # Network commands
        r"(^|\s)(kill|pkill|ps|top|htop|atop|uptime|free)($|\s)",  # Process manipulation commands
        r"(^|\s)(export|unset|set|env)($|\s)",  # Environment variable manipulation commands
        r"(^|\s)(dmesg|uname|hostname|lspci|lsusb|lshw|dmidecode)($|\s)",  # System information commands
        r"(^|\s)(sudo|su|doas|useradd|userdel|usermod|groupadd|groupdel|groupmod|passwd)($|\s)",  # User manipulation commands
        r"(^|\s)(hdparm|fdisk|mount|umount|mkfs|dd|parted)($|\s)",  # Hardware manipulation commands
        r"(^|\s)(install|remove)($|\s)",  # other
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
        result = subprocess.run(
            run_cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output = result.stdout.decode("utf-8")
        start_process(output, shell=True)
        return output
    else:
        print("Unsafe command. Aborting.")
        return None


def term_sgpt(user_input):
    t = threading.Thread(target=run_command, args=(user_input,))
    t.start()


