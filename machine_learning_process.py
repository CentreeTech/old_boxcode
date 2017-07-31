import os
import tensorflow
import librosa
import time, datetime
import av_alsa_process
import numpy as np

#for Sam to work on, though @Kaan we will have to figure out
#how I can signal your process that my process has had an event.
#I think it'll be a Queue in the multiprocessing api.

DATE_STRING = '%Y/%m/%d, %H:%M:%S'

def driver(event_queue, audio_buffer):
	spectrogram = []
	print 'Machine Learning Process beginning.'
	while True:
		if audio_buffer['data'].empty() is False:
			audio_data, video_data = audio_buffer['data'].get()
			#Now we're converting it into a spectrogram
			spectrogram = librosa.feature.melspectrogram(y = np.double(audio_data), sr = av_alsa_process.sample_rate) 
			print '[ML Process] Analyzing Audio.'
			#TENSORFLOW SHIT
			#print 'Tensorflow.'
			probability_crash = 0.9
			
			#put machine learning code heyyah.
			activated = True
			if activated:
				event = 'This was a crash.'
				event_queue['lock'].acquire()
				date_time = datetime.datetime.now().strftime(DATE_STRING)
				event_queue['data'].put((date_time, audio_data, video_data, av_alsa_process.sample_rate, event))
				event_queue['lock'].release()
	return -1
