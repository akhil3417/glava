import os
import shutil
import subprocess


def shellgpt_files_check():
    jarvis_role_file = os.path.expanduser("~/.config/shell_gpt/roles/jarvis.json")
    jarvis_chat_file = os.path.expanduser("~/.cache/shellgpt/jarvis")
    script_file = os.path.join(os.getcwd(), "scripts/jarvis.json")

    if not os.path.exists(jarvis_role_file):
        print(f"Creating Jarvis Role File at {jarvis_role_file}")
        os.makedirs(os.path.dirname(jarvis_role_file), exist_ok=True)
        shutil.copyfile(script_file, jarvis_role_file)

    if not os.path.exists(jarvis_chat_file):
        print("Creating new chat with Jarvis role")
        command = "sgpt --top-p '0.01' --temperature '0.32' --no-cache --role jarvis --chat jarvis"
        subprocess.run(command, shell=True, check=True)


def shellgpt_check():
    try:
        shellgpt_files_check()
    except FileNotFoundError as e:
        print(e)
