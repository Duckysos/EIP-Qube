import pvporcupine
import pyaudio
import numpy as np

# Audio recording parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Number of audio channels (mono)
RATE = 44100              # Sample rate
CHUNK = 512          # Frames per buffer, adjust if necessary
RECORD_SECONDS = 5        # Duration of recording

# Initialize Porcupine
porcupine = pvporcupine.create(
    access_key='YcqT9Njmr3eqJQkf/nZNeDp0k5vX4OOHfvyrdsPf9IChaK36XJxu8w==',
    keyword_paths=["c:\\Users\\user\\OneDrive\\Documents\\GitHub\\EIP-Qube\\Qube\\Hello-Cube_en_windows_v3_0_0.ppn"]
)

# Initialize PyAudio
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Listening...")

try:
    while True:
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            # Convert byte data to int16 using NumPy
            pcm = np.frombuffer(data, dtype=np.int16)
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0:
                print("Hello Cube detected!")
                break  # Exit the inner loop if keyword detected
except KeyboardInterrupt:
    print("Exiting...")

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()
porcupine.delete()


    


    

