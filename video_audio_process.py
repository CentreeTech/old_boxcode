import pyaudio
import time
import numpy as np
import matplotlib.pyplot as plt


CHUNK_SIZE = 1024
BUFFER_LENGTH_SECONDS = 1
RATE = 44100  #this value is whatever the standard for the microphone is. Make sure this is correct for the hardware you have.
BUFFER_LENGTH_VALUES = BUFFER_LENGTH_SECONDS * RATE
CHUNKS_PER_SECOND = RATE / CHUNK_SIZE

pyaudio_object = None;
stream  = None;
data_frames = []

def init_audio(pyaudio_object, stream, rate=44100):
  print "init_audio: Create PyAudio object"
  pyaudio_object = pyaudio.PyAudio()
  print "init_audio: Open stream"
  stream = pyaudio_object.open(input=True,
            channels=1,
            rate=rate,
            format=pyaudio.paFloat32)
  if stream is None:
  	print "IT's FUCKING None"
  print "init_audio: audio stream initialized"
  return pyaudio_object, stream

def close_audio(pyaudio_object, stream):
  print "close_audio: Closing stream"
  if stream is not None:
  	stream.stop_stream()
	stream.close()
  print "close_audio: Terminating PyAudio Object"
  if stream is not None:
	  pyaudio_object.terminate()


#TODO: Kaan focus on this, make a buffer here.
def driver(event_queue, audio_buffer):
	try:
		va_code(event_queue, audio_buffer)
	except Exception,e: 
		print str(e)
		print 'Audio Process Closing due to Error.'
		if stream is not None:
			close_audio(pyaudio_object, stream)
	print 'Audio Process Closing naturally.'
	close_audio(pyaudio_object, stream)


def soundplot(stream, data):
    t1=time.time()
    plt.plot(data)
    plt.title('Yah')
    plt.grid()
    plt.axis([0,len(data),-.001,.001])
    # plt.savefig("03.png",dpi=50)
    # plt.close('all')
    plt.ion()
    print("took %.02f ms"%((time.time()-t1)*1000))

def va_code(event_queue, audio_buffer):
	global pyaudio_object, stream, CHUNK_SIZE
	print 'Video Audio Process beginning.'

	pyaudio_object, stream =  init_audio(pyaudio_object, stream)

	data_frames = []


	# plt.axis([0, 10, 0, 1])
	# plt.ion()
	# plt.pause(0.05)

	while True:
		if stream is None:
			print 'Stream gets broke.'
		try:
			data = stream.read(CHUNK_SIZE, exception_on_overflow = False)
		except Exception,e: 
			print str(e)
		data = np.fromstring(data, 'Float32')
		data_frames.extend(data)

		# plt.plot(data_frames)
		# plt.pause(0.05)
		if len(data_frames) > BUFFER_LENGTH_VALUES:
			print 'Frame finished.'
			#then we need to check if we should create a new buffer
			audio_buffer['data'].put(data_frames)
			soundplot(stream, data_frames)
			data_frames = []
	return -1




