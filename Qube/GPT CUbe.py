import pvcobra
import pvporcupine
import pyaudio
import wave
import numpy as np
import struct
import time
import requests

# Initialize global variables
pv_access_key = 'YcqT9Njmr3eqJQkf/nZNeDp0k5vX4OOHfvyrdsPf9IChaK36XJxu8w=='
custom_keyword_path = "C:\\Users\\iankh\\Documents\\GitHub\\EIP-Qube\\Qube\\Hello-Cube_en_windows_v3_0_0.ppn"
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Number of audio channels (1 for mono)
RATE = 44100              # Sample rate (samples per second)
CHUNK = 1024              # Frames per buffer for Cobra
WAVE_OUTPUT_FILENAME = "output.wav"  # Output file name

def main():
    # Initialize Porcupine for wake word detection
    porcupine = pvporcupine.create(
        access_key=pv_access_key,
        keyword_paths=[custom_keyword_path],
    )
    
    # Initialize Cobra for voice activity detection
    cobra = pvcobra.create(access_key=pv_access_key)
    
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    print("Listening for wake word...")
    detect_wake_word(stream, porcupine)

    print("Wake word detected. Recording...")
    frames = record_until_silence(stream, cobra)

    # Cleanup
    stream.stop_stream()
    stream.close()
    audio.terminate()
    porcupine.delete()
    cobra.delete()
    
    # Save the recorded data as a WAV file
    save_recording(frames)

def detect_wake_word(stream, porcupine):
    while True:
        data = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, data)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            break

def record_until_silence(stream, cobra, silence_threshold=1.3):
    frames = []
    last_voice_time = time.time()
    
    while True:
        data = stream.read(cobra.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * cobra.frame_length, data)
        if cobra.process(pcm) > 0.5:  # Adjust voice activity threshold if needed
            last_voice_time = time.time()
            frames.append(data)
        else:
            if (time.time() - last_voice_time) > silence_threshold:
                print("End of speech detected.")
                break
    
    return frames

def save_recording(frames):
    print("Saving recording...")
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Recording saved to {WAVE_OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()