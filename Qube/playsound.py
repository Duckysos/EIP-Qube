import wave
import pyaudio

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

file_path = "C:/Users/iankh/Documents/GitHub/EIP-Qube/Qube/output.wav"
play_audio(file_path)