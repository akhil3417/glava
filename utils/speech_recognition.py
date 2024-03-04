import websockets
import logging
import json
import asyncio
import subprocess


async def listen(uri, is_listening):
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
                # if 'text' in transcript_dict and transcript_dict['text'].startswith("hey"):
                if len(transcript_dict.get("text", "")) > 4 and "text" in transcript:
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
    listen_task = asyncio.create_task(listen(uri, is_listening))
    return listen_task


def stop_listening():
    global is_listening
    global listen_task
    is_listening = False
    listen_task.cancel()
