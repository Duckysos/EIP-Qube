import threading
import subprocess

class VideoPlayer(threading.Thread):

    def __init__(self, videos):
        threading.Thread.__init__(self)
        self.videos = videos
        self.current_state = None
        self.next_state = None
        self.running = True

    def run(self):
        while self.running:
            if self.next_state != self.current_state:
                self.current_state = self.next_state
                video_path = self.videos.get(self.current_state)
                if video_path:
                    self.play_video(video_path)

    def play_video(self, video_path):
        # Use VLC to play video
        subprocess.call(['cvlc', '--play-and-exit', video_path])

    def change_state(self, new_state):
        self.next_state = new_state

    def stop(self):
        self.running = False

# Video files for different states
videos = {
    'state1': '/home/pi/EIP-Qube/videos/Mousey Answer Correct.avi',
    'state2': '/home/pi/EIP-Qube/videos/Mousey Idle.avi',
    'state3': '/home/pi/EIP-Qube/videos/Mousey Listening.avi',
    'state4': '/home/pi/EIP-Qube/videos/Mousey Waiting(Loading).avi',
    'state5': '/home/pi/EIP-Qube/videos/Mousey Wrong Answer.avi'
}

if __name__ == '__main__':
    # Initialize the video player with the state-video mapping
    player = VideoPlayer(videos)
    player.start()

    # Example of changing states
    player.change_state('state1')
    # Wait or perform other tasks...
    player.change_state('state2')
    # Continue with your application logic...

    # Stop the video player when done
    player.stop()
    player.join()