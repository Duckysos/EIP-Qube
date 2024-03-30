import vlc
import time


video_path = "C:\\Users\\user\\OneDrive\\Documents\\GitHub\\EIP-Qube\\videos\\Test.mp4"
player = vlc.Instance('--fullscreen')
media_player = player.media_player_new()
media = player.media_new(video_path)
media_player.set_media(media)
media_player.play()
time.sleep(1)

while media_player.is_playing():
    time.sleep(1)  # Wait for the video to finish
