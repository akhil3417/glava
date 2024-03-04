import re
import subprocess

from rich import print
from rich.prompt import Prompt
from prompt_toolkit import prompt

# from skills.online import send_email
from .input_output import (
    send_notification,
    speak_or_print,
    start_process,
    run_shell_command_and_return_output,
)


def is_command_safe(cmd):
    unsafe_patterns = [
        r"rm\s+-[rRf]",  # Remove command
        r";",  # Command separator
        r"\|",  # Pipe
        r"&",  # Background process
        r"(^|\s)(cat|cd|chmod|chown|cp|df|diff|du|find|fmt|grep|less|ln|ls|make|mkdir|mv|rm|sed|sort|tail|tar|touch|uniq|vi|wc)($|\s)",  # File manipulation commands
        r"(^|\s)(curl|wget|ssh|ftp|ping|telnet)($|\s)",  # Network commands
        r"(^|\s)(kill|pkill|ps|free)($|\s)",  # Process manipulation commands
        r"(^|\s)(export|unset|set|env)($|\s)",  # Environment variable manipulation commands
        r"(^|\s)(dmesg|uname|hostname|lspci|lsusb|lshw|dmidecode)($|\s)",  # System information commands
        r"(^|\s)(sudo|su|doas|useradd|userdel|usermod|groupadd|groupdel|groupmod|passwd)($|\s)",  # User manipulation commands
        r"(^|\s)(hdparm|fdisk|mount|umount|mkfs|dd|parted)($|\s)",  # Hardware manipulation commands
        r"(^|\s)(install|remove|path|to)($|\s)",  # other
    ]
    result = subprocess.run(
        cmd,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = result.stdout.decode("utf-8")
    cleaned_output = remove_markdown_formatting(output)
    print(
        f"[bold green]Generated Command[/bold green]:[bold yellow] {cleaned_output}[/bold yellow]"
    )
    for pattern in unsafe_patterns:
        if re.search(pattern, cleaned_output):
            print(
                f"[bold green]Aborted Unsafe Generated Command[/bold green]:[bold yellow] {cleaned_output}[/bold yellow]"
            )
            return None
    send_notification("Running", cleaned_output)
    return cleaned_output


def remove_markdown_formatting(text):
    # markdown_formatting_codes = r"(\*|\~|\`|\||\_|\#|\+|\-|\!|\[|\]|\(|\)|\.|\>|\<|\=)"
    markdown_formatting_codes = r"(\bash|\n|\`|\```|\*)"
    return re.sub(markdown_formatting_codes, "", text)


def sgpt_shell_ai(user_input):
    run_cmd = f"sgpt -s --no-cache --no-interaction --role commandonly '{user_input}'"
    cmd = is_command_safe(run_cmd)
    if cmd:
        start_process(cmd, shell=True)


def term_sgpt(user_input):
    run_cmd = f"sgpt --no-cache --role commandonly '{user_input}'"
    # run_cmd = f"sgpt -s --no-interaction --chat command '{user_input}'"
    print(
        f"[bold green]Requested command[/bold green]: [bold yellow]{run_cmd}[/bold yellow]"
    )
    #  NOTE 2024-03-03: since this is func is Interactive , disable is_command_safe check
    # output = is_command_safe(run_cmd)

    result = subprocess.run(run_cmd, shell=True, check=True, capture_output=True)
    output = result.stdout.decode("utf-8")
    output = remove_markdown_formatting(output)
    print(
        f"[bold green]Generated Command[/bold green]:[bold yellow] {output}[/bold yellow]"
    )
    if output:
        confirmation = Prompt.ask(
            "[bold red]Choose to proceed further?:[/bold red][bold yellow]execute, abort, edit[/bold yellow] ",
            choices=["c", "a", "e"],
        )
        if confirmation.lower() == "c":
            run_shell_command_and_return_output(output, shell=True, print_output=True)
        elif confirmation.lower() == "e":
            print("[bold blue]Please modify the command :[/bold blue]", end=" ")
            modified_command = prompt("", default=output)
            confirmation = "yes"  # Default to "yes" for simplicity
            if confirmation.lower() == "yes":
                run_shell_command_and_return_output(
                    modified_command, shell=True, print_output=True
                )
            else:
                print("[bold red]Command not confirmed. Aborting.[/bold red]")
                return None
        else:
            print("[bold red]Aborting.[/bold red]")
            return None


