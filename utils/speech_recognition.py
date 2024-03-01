import websockets
import logging
import json
import asyncio
import subprocess


async def listen(uri, is_listening):
    async with websockets.connect(uri) as websocket:
        while is_listening:
            try:
                transcript = await websocket.recv()
                transcript_dict = json.loads(transcript)
                # if 'text' in transcript_dict and transcript_dict['text'].startswith("hey"):
                if len(transcript_dict.get('text', '')) > 10 and 'text' in transcript:
                    with open("/tmp/transcript.txt", "w") as f:
                        f.write(transcript_dict['text'])
                    print(f"User:",transcript_dict['text'])
                    return

            except json.JSONDecodeError:
                logging.warning(f"Received non-JSON transcript: {transcript}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
async def start_listening(uri, is_listening):
    listen_task = asyncio.create_task(listen(uri, is_listening))
    return listen_task


def stop_listening():
    global is_listening
    global listen_task
    is_listening = False
    listen_task.cancel()
