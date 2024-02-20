import pvcobra
import pyaudio
import numpy as np
import struct
import time

pv_access_key = 'YcqT9Njmr3eqJQkf/nZNeDp0k5vX4OOHfvyrdsPf9IChaK36XJxu8w=='

'''
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
'''


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