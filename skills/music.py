import subprocess
from shutil import which
import re

from utils.input_output import speak_or_print, take_command

from .yt import get_media_url, play


def play_audio(user_input):
    media_url = get_media_url(user_input, 1)

    # Extract the video ID from the URL using regex
    video_id = re.search(r"v=(\w+)", media_url).group(1)

    # check if mpc is available
    mpc = which("mpc")
    if mpc is not None:
        cmd = [mpc, "add"]
    else:
        mpv = which("mpv")
        if mpv is not None:
            cmd = [mpv]
        else:
            raise Exception("Neither mpc nor mpv found")

    cmd.append(
        subprocess.check_output(
            ["yt-dlp", "--prefer-insecure", "-g", "-f251", video_id]
        )
        .decode()
        .strip()
    )

    subprocess.call(cmd)


def play_video(user_input):
    media_url = get_media_url(user_input, 1)
    play(media_url, "-v")


def stream_yt(user_input):
    if "video" in user_input:
        play_video(user_input)
    else:
        play_audio(user_input)


async def query_run_stream_async():
    speak_or_print("What do you want to play? ")
    await take_command()
