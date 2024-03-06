import websockets
import logging
import json
import asyncio
import subprocess
from config import WAKEWORD as wakeword


async def listen(uri, is_listening):
    """
    A coroutine function to listen on a given URI for incoming messages and process them accordingly.

    Args:
        uri (str): The URI to connect to.
        is_listening (bool): A flag to indicate if the function should continue listening for messages.

    Returns:
        None
    """
    # Check if any aplay process is running
    aplay_check = subprocess.run(["pgrep", "-x", "aplay"], capture_output=True)
    while aplay_check.returncode == 0:
        # If aplay is running, wait for it to complete
        await asyncio.sleep(1)
        # Re-check
        aplay_check = subprocess.run(["pgrep", "-x", "aplay"], capture_output=True)

    async with websockets.connect(uri) as websocket:
        while is_listening:
            try:
                transcript = await websocket.recv()
                transcript_dict = json.loads(transcript)
                if "text" in transcript_dict and (
                    wakeword in transcript_dict["text"]
                    or len(transcript_dict.get("text", "")) > 20
                ):
                    transcript_dict["text"] = transcript_dict["text"].replace(
                        wakeword, ""
                    )

                    with open("/tmp/transcript.txt", "w") as f:
                        f.write(transcript_dict["text"])
                    print(f"User:", transcript_dict["text"])
                    return

            except json.JSONDecodeError:
                logging.warning(f"Received non-JSON transcript: {transcript}")
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                break
async def start_listening(uri, is_listening):
    """
    Asynchronous function that starts listening on the given URI.

    Args:
        uri: The URI to listen on.
        is_listening: A boolean indicating whether the function is currently listening.

    Returns:
        A task object representing the listening process.
    """
    listen_task = asyncio.create_task(listen(uri, is_listening))
    return listen_task


def stop_listening():
    """
    Stops the listening process by setting the is_listening flag to False and canceling the listen_task.
    """
    global is_listening
    global listen_task
    is_listening = False
    listen_task.cancel()
