from .yt import get_media_url, play
from utils.input_output import (
    speak_or_print,
    take_command,
)


def play_audio(user_input):
    media_url = get_media_url(user_input, 1)
    play(media_url, "--ytdl-format=bestaudio --no-video")


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
