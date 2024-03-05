import subprocess
from shutil import which
from urllib.parse import urlparse, parse_qs

from utils.input_output import speak_or_print, take_command
from .yt import get_media_url, play


def get_video_id(url):
    query = urlparse(url).query
    params = parse_qs(query)
    return params["v"][0]


def play_audio(user_input):
    media_url = get_media_url(user_input, 1)
    video_id = get_video_id(media_url)

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
    # if we are using mpc, play the playlist
    if mpc is not None:
        subprocess.call([mpc, "play"])


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
