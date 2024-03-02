import os
import re
import subprocess
import threading
from rich import print
from rich.prompt import Prompt

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
    result = subprocess.run(
        cmd,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = result.stdout.decode("utf-8")
    for pattern in unsafe_patterns:
        if re.search(pattern, output):
            print(f"Unsafe command {output}. Aborting.")
            return None
    # If the command is safe, run it
    cleaned_output = remove_markdown_formatting(output)
    send_notification("Generated Command", cleaned_output)
    return output


def sgpt_shell_ai(user_input):
    run_cmd = f"sgpt --no-cache --role commandonly '{user_input}'"
    is_command_safe(run_cmd)


def run_command(user_input):
    run_cmd = f"sgpt --no-cache --role commandonly '{user_input}'"
    # run_cmd = f"sgpt -s '{user_input}'"
    output = is_command_safe(run_cmd)
    if output is not None:
        print(
            f"[bold green]Requested command[/bold green]: [bold yellow]{run_cmd}[/bold yellow]"
        )
        print(
            f"[bold green]Generated Command[/bold green]:[bold yellow] {output}[/bold yellow]"
        )
        confirmation = Prompt.ask(
            "[bold red]Choose to proceed further?:[/bold red]",
            choices=["execute", "abort", "edit"],
        )
        if confirmation.lower() == "execute":
            subprocess.run(output, shell=True)
            return output
        elif confirmation.lower() == "edit":
            print("[bold blue]Please modify the command below:[/bold blue]")
            modified_command = prompt("Edit the command: ", default=output)
            confirmation = "yes"  # Default to "yes" for simplicity
            if confirmation.lower() == "yes":
                subprocess.run(modified_command, shell=True)
                return modified_command
            else:
                print("[bold red]Command not confirmed. Aborting.[/bold red]")
                return None
        else:
            print("[bold red]Aborting.[/bold red]")
            return None


def term_sgpt(
    user_input,
):  #  TODO 2024-03-01:implement executing cli shell commands in new term
    t = threading.Thread(target=run_command, args=(user_input,))
    t.start()


