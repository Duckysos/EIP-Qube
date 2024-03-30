import threading
import subprocess
import vlc
import time

def play_video(video_path):
    def video_thread():
        player = vlc.MediaPlayer()
        media = vlc.Media(video_path, "file-caching =10000")
        player.set_media(media)
        player.play()
        # Keep running until the video is playing
        while player.is_playing():
            time.sleep(1)
        player.stop()

    thread = threading.Thread(target=video_thread)
    thread.start()

if __name__ == '__main__':
    play_video("C:\\Users\\user\\OneDrive\\Documents\\GitHub\\EIP-Qube\\videos\\Test.mp4")