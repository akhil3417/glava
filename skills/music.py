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

