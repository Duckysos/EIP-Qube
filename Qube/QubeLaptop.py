import pvcobra
import pvporcupine
import pyaudio
import wave
import numpy as np
import struct
import time
import requests
from pydub import AudioSegment
from pydub.playback import play
import vlc
import threading


api_url = "https://2ac3-82-132-234-200.ngrok-free.app/audio_to_audio"
headers = {
     'ngrok-skip-browser-warning':'69420'
}
cobra = None
porcupine = None
audio = None
audio_stream = None
pv_access_key = '3P4D65EChSMd5ugsHg7sn62wFivcgd0wFRHrqXvgnPJngvqdwZ4RBw=='
custom_keyword_path = "/home/pi/EIP-Qube/Qube/Hello-Cube_en_windows_v3_0_0.ppn"
file_path = "/home/pi/EIP-Qube/audio.wav"
download_path = "/home/pi/EIP-Qube/Qube/downloaded_audio.wav"
video_path = ""
is_conversation_mode = False
playback_active = True

# Audio recording parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Number of audio channels (1 for mono, 2 for stereo)
RATE = 40000             # Sample rate (samples per second)
CHUNK = 1024              # Number of frames per buffer
RECORD_SECONDS = 5        # Duration of recording
WAVE_OUTPUT_FILENAME = "audio.wav"  # Output file name


def toggle_conversation_mode():
    global is_conversation_mode
    is_conversation_mode = not is_conversation_mode
    if is_conversation_mode:
        print("Entering conversation mode...")
    else:
        print("Exiting conversation mode...")

def initialize_porcupine():
    porcupine = pvporcupine.create(
        access_key=pv_access_key,
        keyword_paths=[custom_keyword_path]
    )
    return porcupine

def intialize_audio_stream(porcupine):
    audio = pyaudio.PyAudio()
    audio_stream = audio.open(format=pyaudio.paInt16, channels=1,
                              rate=porcupine.sample_rate, input=True,
                              frames_per_buffer=porcupine.frame_length)
    return audio, audio_stream

def detect_wake_word (porcupine, audio_stream):
    # Listen for the wake word
    print("Listening for wake word...")
    while True:
        data = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, data)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Hello Cube detected!")
            toggle_conversation_mode()
            audio_stream.stop_stream()
            audio_stream.close()
            return True

def play_audio(file_path):
     audio = AudioSegment.from_file(file_path)
     play(audio)



def listen():

    cobra = pvcobra.create(access_key=pv_access_key)

    listen_pa = pyaudio.PyAudio()

    listen_audio_stream = listen_pa.open(
                rate=cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=cobra.frame_length)

    print("Listening...")

    while True:
        listen_pcm = listen_audio_stream.read(cobra.frame_length)
        listen_pcm = struct.unpack_from("h" * cobra.frame_length, listen_pcm)
           
        if cobra.process(listen_pcm) > 0.3:
            print("Voice detected")
            listen_audio_stream.stop_stream
            listen_audio_stream.close()
            cobra.delete()
            break


def listen_until_silence():
        frames = []
        last_voice_time = time.time()
        silence_threshold = 1.5
        cobra = pvcobra.create(access_key=pv_access_key)
        silence_pa = pyaudio.PyAudio()
        audio = pyaudio.PyAudio()

        cobra_stream = silence_pa.open(
                rate=cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=cobra.frame_length)
        
        stream = audio.open(
                    format=FORMAT, 
                    channels=CHANNELS,
                    rate=RATE, 
                    input=True,
                    frames_per_buffer=CHUNK)
        
        # Record audio until silence
        while True:
            data = stream.read(CHUNK)
            cobra_pcm = cobra_stream.read(cobra.frame_length, exception_on_overflow=False)
            cobra_pcm = struct.unpack_from("h" * cobra.frame_length, cobra_pcm)
            frames.append(data)
            print(cobra.process(cobra_pcm))
            if cobra.process(cobra_pcm) > 0.1:
                last_voice_time = time.time()
            else:
                if(time.time() - last_voice_time) > silence_threshold:
                    print("End of speech detected.")
                    break

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded data as a WAV file
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

def send_audio_file():
    with open (file_path, 'rb') as f:

        files = {'file': ('audio.wav', f, 'audio/wav')}

        response = requests.post(api_url, headers=headers, files=files) 

        # Check if the request was successful (status code 200) 

        if response.status_code == 200:
            audio_content = response.content 
            with open (download_path,'wb') as f:
                f.write(audio_content)
            print("File upload successfully.")

        else: 

    # Print an error message if the request was not successful 
            print(f"Error: {response.status_code} - {response.text}")

def play_video(video_path):
    global playback_active
    player = vlc.Instance('--fullscreen')
    media_player = player.media_player_new()
    media = player.media_new(video_path)
    media_player.set_media(media)
    media_player.play()

    # Wait for the video to initialize
    time.sleep(1)

    # Loop to keep checking if playback should stop
    while media_player.is_playing() and playback_active:
        time.sleep(1)

    # Stop the video if the loop ends
    media_player.stop()

try:
    playback_thread = threading.Thread(target=play_video, args=("C:\\Users\\user\\OneDrive\\Documents\\GitHub\\EIP-Qube\\videos\\Mousey Answer Correct.avi"))
    playback_thread.start()
    play_audio("/home/pi/EIP-Qube/PowerOn.wav")
    while True:
        if not is_conversation_mode:
            # Listening for the wake word
            initial_porcupine = initialize_porcupine()
            audio, audio_stream = intialize_audio_stream(initial_porcupine)
            detect_wake_word(initial_porcupine, audio_stream)
        else:
            # In conversation mode, record, send, and play response
            listen()
            print("Recording...")
            listen_until_silence()
            send_audio_file()
            play_audio(download_path)
except KeyboardInterrupt:
    play_audio("/home/pi/EIP-Qube/PowerOff.wav")
    print("Program exited by user.")