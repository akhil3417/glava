import subprocess
from config import IS_LISTENING
from utils.input_output import ask_for_input, speak_or_print,take_command

# stream music(aud vid)
# def play_song_and_write_transcript(song_to_play, script='/home/shiva/.local/bin/vosk-music'):
def play_song_and_write_transcript(song_to_play):
    # Write song to play to transcript file
    with open('/tmp/transcript.txt', 'w') as f:
        f.write(song_to_play)

    # # Define default script
    script = 'y'

    # If "audio" keyword is in the transcript.txt , use 'vosk_music' script
    if 'audio' in song_to_play.lower():
          script = '/home/shiva/.local/bin/vosk-music'
    # Run music script
    subprocess.run([script, song_to_play], check=True)

# def play_command(user_input , script='/home/shiva/gitclones/jarvis-repos/linux-assistant/skills/yt.py'):
def play_song(user_input):
    play_song_and_write_transcript(user_input)

async def stream_with_listen(user_input):
    song_to_play = await ask_for_input('What do you want to play?')
    play_song_and_write_transcript(song_to_play)

def stream_without_listen(user_input):
    song_to_play = input('What do you want to play? ')
    play_song_and_write_transcript(song_to_play)

async def run_stream_async(user_input):
    speak_or_print('What do you want to play? ')
    query = await take_command()
    print(f"Playing",query)
    if IS_LISTENING:
        play_song_and_write_transcript(query)
    else:
        play_song_and_write_transcript(query)
