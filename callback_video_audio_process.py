import pyaudio
import numpy as np

CHUNK_SIZE = 2**10
BUFFER_LENGTH_SECONDS = 1
RATE = 44100  #this value is whatever the standard for the microphone is. Make sure this is correct for the hardware you have.
BUFFER_LENGTH_VALUES = BUFFER_LENGTH_SECONDS * RATE

def callback(in_data, frame_count, time_info, flag):
    if flag:
        print("Playback Error: %i" % flag)
    played_frames = callback.counter
    callback.counter += frame_count
    limiter.limit(signal[played_frames:callback.counter], threshold)
    return signal[played_frames:callback.counter], paContinue


#open the stream
pa = PyAudio()

stream = pa.open(format = pyaudio.paFloat32,
                 channels = 1,
                 rate = RATE,
                 frames_per_buffer = CHUNK_SIZE,
                 output = True,
                 stream_callback = callback)


while stream.is_active():
    sleep(1)

stream.close()
pa.terminate()