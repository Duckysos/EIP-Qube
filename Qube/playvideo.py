import subprocess
import time

# Function to play video using VLC
def play_video(video_path):
    # Using the cvlc command to play the video
    # Adding '--play-and-exit' to make sure VLC closes after playing the video
    subprocess.run(['cvlc', '--play-and-exit', video_path])

# Example program state
program_state = 'state1'

# Video files for different states
videos = {
    'state1': 'C:\\Users\\iankh\\Documents\\GitHub\\EIP-Qube\\videos\\Mousey Answer Correct.avi',

}

# Play the video based on the program state
if program_state in videos:
    play_video(videos[program_state])
else:
    print("No video for the current state.")