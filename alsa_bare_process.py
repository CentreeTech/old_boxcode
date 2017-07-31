import alsaaudio
import audioop
import time
import numpy
import io
import picamera
import ffmpy

sample_rate = 16000
BLOCK_SIZE = 3 #this is the number of seconds we do chunks for.

def driver(event_queue, audio_buffer):
	print 'Beginning Audio Process.'
	
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
	inp.setchannels(1)
	inp.setrate(sample_rate)
	inp.setperiodsize(512)
	packet_buffer = []
	temp_buffer = []
	packet_buffer_size = sample_rate*BLOCK_SIZE #this is the buffer to be sent to the next process
	
	video_stream = io.BytesIO()
	with picamera.PiCamera() as camera:
		camera.resolution = (640, 480)
		camera.start_recording(video_stream, format='h264', quality=23)
		while 1:
			l,data = inp.read()
			if l:
				for i in range(len(data)/2):
					temp_buffer.append(audioop.getsample(data, 2, i))

				if (len(temp_buffer) + len(packet_buffer) > packet_buffer_size):
					samples_to_copy = packet_buffer_size - len(packet_buffer)
				else:
					samples_to_copy = len(temp_buffer)
			
				packet_buffer = packet_buffer + temp_buffer[0:samples_to_copy];
				del(temp_buffer[0:samples_to_copy])

				if len(packet_buffer) == packet_buffer_size:
					#start pushing shit
					print '[AV Process] Recorded audio/video chunk.'
					camera.stop_recording()
					video_stream = io.BytesIO()
					audio_buffer['lock'].acquire()
					audio_buffer['data'].put( (packet_buffer, video_stream) )
					audio_buffer['lock'].release()
					video_stream = io.BytesIO()
					camera.start_recording(video_stream, format='h264', quality=23)
					packet_buffer = []
