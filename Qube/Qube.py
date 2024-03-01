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
custom_keyword_path = "C:/Users/iankh/Documents/GitHub/EIP-Qube/Qube/Hello-Cube_en_windows_v3_0_0.ppn"


# Audio recording parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Number of audio channels (1 for mono, 2 for stereo)
RATE = 40000             # Sample rate (samples per second)
CHUNK = 1024              # Number of frames per buffer
RECORD_SECONDS = 5        # Duration of recording
WAVE_OUTPUT_FILENAME = "output.wav"  # Output file name

def play_audio(file_path):
    # Open the WAV file
    wf = wave.open(file_path, 'rb')

    # Create a PyAudio object
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data in chunks
    chunk_size = 1024
    data = wf.readframes(chunk_size)

    # Play the audio file
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Close PyAudio
    p.terminate()


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
        play_audio("C:/Users/iankh/Documents/GitHub/EIP-Qube/Qube/output.wav")

        break

