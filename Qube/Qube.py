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
AudioSegment.converter = r"C:/Users/user/OneDrive/Desktop/ffmpeg-2024-03-04-git-e30369bc1c-essentials_build/bin"

api_url = "https://5fd3-92-237-138-59.ngrok-free.app/audio_to_audio"
headers = {
     'ngrok-skip-browser-warning':'69420'
}
cobra = None
porcupine = None
audio = None
audio_stream = None
pv_access_key = '3P4D65EChSMd5ugsHg7sn62wFivcgd0wFRHrqXvgnPJngvqdwZ4RBw=='
custom_keyword_path = "C:/Users/user/OneDrive/Documents/GitHub/EIP-Qube/Qube/Hello-Cube_en_windows_v3_0_0.ppn"



# Audio recording parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Number of audio channels (1 for mono, 2 for stereo)
RATE = 40000             # Sample rate (samples per second)
CHUNK = 1024              # Number of frames per buffer
RECORD_SECONDS = 5        # Duration of recording
WAVE_OUTPUT_FILENAME = "audio.wav"  # Output file name


def play_audio(file_path):
     audio = AudioSegment.from_file(file_path)
     play(audio)

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
    
def wake_word():
    
    # Initialize Porcupine
    porcupine = pvporcupine.create(
        access_key= pv_access_key,
        keyword_paths= [custom_keyword_path],
    )


    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    audio_stream = audio.open(format=pyaudio.paInt16, channels=1,
                    rate=porcupine.sample_rate, input=True,
                    frames_per_buffer=porcupine.frame_length)

    print("Listening...")


    try:
        while True:
                data = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, data)
                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    print("Hello Cube detected!")
                    audio_stream.stop_stream()
                    audio_stream.close()
                    porcupine.delete()
                    break  # Exit the inner loop if keyword detected
    except KeyboardInterrupt:
        print("Exiting...")

def send_audio_file():
    file_path = "C:/Users/user/OneDrive/Documents/GitHub/EIP-Qube/audio.wav"
    download_path = "C:/Users/user/OneDrive/Documents/GitHub/EIP-Qube/Qube/downloaded_audio.wav"
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

try:
    while True:
        wake_word()
        # Initialize pyaudio
        audio = pyaudio.PyAudio()

        # Open stream for recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        print("Recording...")
        listen_until_silence()
        send_audio_file() 
        play_audio("C:/Users/user/OneDrive/Documents/GitHub/EIP-Qube/Qube/downloaded_audio.wav")

except KeyboardInterrupt:
    print("Program exited by user.")