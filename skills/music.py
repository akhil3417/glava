import subprocess
from shutil import which
from urllib.parse import urlparse, parse_qs

from utils.input_output import speak_or_print, take_command, send_notification
from .yt import get_media_url, play


def get_video_id(url):
    """
    Get the video ID from the given URL.

    Parameters:
    url (str): The URL of the video.

    Returns:
    str: The video ID extracted from the URL.
    """
    query = urlparse(url).query
    params = parse_qs(query)
    return params["v"][0]


def play_audio(user_input):
    """
    Play an audio file based on the user input.

    Args:
        user_input (str): The user input to determine the media URL and video ID.

    Raises:
        Exception: If neither mpc nor mpv is found.

    Returns:
        None
    """
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

    # send notification
    send_notification("Playing Audio", f"Playing audio from {media_url}")


def play_video(user_input):
    """
    Function to play a video based on user input.

    Args:
        user_input (str): The user input to determine the video to play.

    Returns:
        None
    """
    media_url = get_media_url(user_input, 1)
    play(media_url, "-v")

    # send notification
    send_notification("Playing Video", f"Playing video from {media_url}")


def stream_yt(user_input):
    """
    Function to stream content based on user input.

    Parameters:
    user_input (str): The input provided by the user.

    Returns:
    None
    """
    if "video" in user_input:
        play_video(user_input)
    else:
        play_audio(user_input)


async def query_run_stream_async():
    """
    Asynchronous function to run a stream of queries.
    """
    speak_or_print("What do you want to play? ")
    await take_command()
