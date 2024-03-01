import pvcobra
import pvporcupine
import pyaudio
import wave
import numpy as np
import struct
import time
import requests 

api_url = "https://0988-185-92-25-79.ngrok-free.app"
headers = {
     'ngrok-skip-browser-warning':'69420'
}
cobra = None
porcupine = None
audio = None
audio_stream = None
pv_access_key = 'YcqT9Njmr3eqJQkf/nZNeDp0k5vX4OOHfvyrdsPf9IChaK36XJxu8w=='
custom_keyword_path = "C:\\Users\\user\\OneDrive\\Documents\\GitHub\\EIP-Qube\\Qube\\Hello-Cube_en_windows_v3_0_0.ppn"


# Audio recording parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Number of audio channels (1 for mono, 2 for stereo)
RATE = 44100              # Sample rate (samples per second)
CHUNK = 1024              # Number of frames per buffer
RECORD_SECONDS = 5        # Duration of recording
WAVE_OUTPUT_FILENAME = "output.wav"  # Output file name


def listen_until_silence():
        frames = []
        last_voice_time = time.time()
        silence_threshold = 1.3
        cobra = pvcobra.create(access_key=pv_access_key)
        # Record audio until silence
        while True:
            data = stream.read(cobra.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * cobra.frame_length, data)
            if cobra.process(pcm) > 0.5:
                last_voice_time = time.time()
                frames.append(data)
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

def detect_silence():

    cobra = pvcobra.create(access_key=pv_access_key)

    silence_pa = pyaudio.PyAudio()

    cobra_audio_stream = silence_pa.open(
                    rate=cobra.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=cobra.frame_length)

    last_voice_time = time.time()

    while True:
        cobra_pcm = cobra_audio_stream.read(cobra.frame_length)
        cobra_pcm = struct.unpack_from("h" * cobra.frame_length, cobra_pcm)
           
        if cobra.process(cobra_pcm) > 0.2:
            last_voice_time = time.time()
        else:
            silence_duration = time.time() - last_voice_time
            if silence_duration > 1.3:
                print("End of query detected\n")
                cobra_audio_stream.stop_stream                
                cobra_audio_stream.close()
                cobra.delete()
                last_voice_time=None
                break

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

        response = requests.get(f"{api_url}/getAllLessons", headers=headers)
        
        if response.status_code == 200:
             print(response.json())

        else:
             print(f"Error: {response.status_code} - {response.text}") 
        break

