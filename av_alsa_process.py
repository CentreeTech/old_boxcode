import alsaaudio
import audioop
import time
import numpy

#from picamera.array import PiRGBArray
#from picamera import PiCamera
#import cv2

sample_rate = 16000
activationDetection = True
minActivityDuration = 1.0

def driver(event_queue, audio_buffer, config_data):
	global sample_rate
	print 'Beginning Audio Process.'
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
	inp.setchannels(1) 				#1 channel
	inp.setrate(sample_rate)                        # set sampling freq
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)      # set 2-byte sample
	inp.setperiodsize(512)
	curWindow = []	
	BLOCKSIZE = 1
	midTermBufferSize = int(sample_rate*BLOCKSIZE)
	midTermBuffer = []
	timeStart = time.time()
	curActiveWindow = numpy.array([])
	allData = []
	count = 0
	energy100_buffer_zero = []

	while 1:
		l, data = inp.read()
    		if l:
			for i in range(len(data)/2):
				curWindow.append(audioop.getsample(data, 2, i))
			if (len(curWindow)+len(midTermBuffer)>midTermBufferSize):
				samplesToCopyToMidBuffer = midTermBufferSize - len(midTermBuffer)
			else:
				samplesToCopyToMidBuffer = len(curWindow)
			
			midTermBuffer = midTermBuffer + curWindow[0:samplesToCopyToMidBuffer]
			del(curWindow[0:samplesToCopyToMidBuffer])
			
			if len(midTermBuffer) == midTermBufferSize:
				elapsedTime = (time.time() - timeStart)
				dataTime = (count+1) * BLOCKSIZE

				allData += midTermBuffer
				sendBuffer = midTermBuffer
				midTermBuffer = numpy.double(midTermBuffer)
				activated = False
				if activationDetection:
					energy100 = (100*numpy.sum(midTermBuffer * midTermBuffer) / (midTermBuffer.shape[0] * 32000 * 32000))     
					if count < 10:                                                          # TODO make this param
	                        		energy100_buffer_zero.append(energy100)                    
	                        		mean_energy100_zero = numpy.mean(numpy.array(energy100_buffer_zero))
	                    		else:
	                        		mean_energy100_zero = numpy.mean(numpy.array(energy100_buffer_zero))
	                        		if (energy100 < 1.2 * mean_energy100_zero):
	                            			if curActiveWindow.shape[0] > 0:                                    # if a sound has been detected in the previous segment:
	                                			activeT2 = elapsedTime - BLOCKSIZE                              # set time of current active window
								if activeT2 - activeT1 > minActivityDuration:
	                                    				if activationDetection:
	                                        				activated = True
										print 'YAh'
	                                			curActiveWindow = numpy.array([])                               # delete current active window
	                        		else:
	                            			if curActiveWindow.shape[0] == 0:                                   # this is a new active window!
	                                			activeT1 = elapsedTime - BLOCKSIZE                              # set timestamp start of new active window
	                            			curActiveWindow = numpy.concatenate((curActiveWindow, midTermBuffer))
	
				audio_buffer['data'].put( (sendBuffer, activated) )
				midTermBuffer = []
				count += 1
								

