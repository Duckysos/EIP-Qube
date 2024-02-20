import pvporcupine
import pyaudio
import numpy as np
import struct


porcupine = None
audio = None
audio_stream = None
pv_access_key = 'YcqT9Njmr3eqJQkf/nZNeDp0k5vX4OOHfvyrdsPf9IChaK36XJxu8w=='
custom_keyword_path = "C:\\Users\\iankh\\Documents\\GitHub\\EIP-Qube\\Qube\\Hello-Cube_en_windows_v3_0_0.ppn"
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
            # Convert byte data to int16 using NumPy
            pcm = struct.unpack_from("h" * porcupine.frame_length, data)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Hello Cube detected!")
                break  # Exit the inner loop if keyword detected
except KeyboardInterrupt:
    print("Exiting...")

# Cleanup
audio_stream.stop_stream()
audio_stream.close()
audio.terminate()
porcupine.delete()


    

