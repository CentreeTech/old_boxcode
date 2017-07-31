import multiprocessing

import machine_learning_process
import server_communication_process
import alsa_bare_process
import av_alsa_process

#is booted at start and begins all other processes.
#double checks the health of other processes and makes sure that they are running correctly.


#I need to figure out a logging feature to log when things go down. Some kind of global Queue that 
#can be held by the watchdog, added to by the other processes, and sent to the server by the server_communication process.


AUDIO_BUFFER_SIZE = 500
CONFIG_FILE = 'CENTREE.CONFIG'


# This part begins the whole process of creating processes, running them, and then checking if they're still alive or if they've died.

#sam will deal with this	

if __name__ == "__main__":
	#this is where we create the processes

	#SHARED MEMORY AND MUTEX LOCKS
	
	#config_data = {'data' : update_config(),
	#				'lock' : multiprocessing.Lock()}
	audio_buffer = { 'data' : multiprocessing.Queue(), #the current audio buffer, shared by all processes.
					 'lock' : multiprocessing.Lock()}

	event_queue = { 'data' : multiprocessing.Queue(),   #this is the queue of events created by the ML process,
					'lock' : multiprocessing.Lock() }		 #they are processed by the server_communication process.
	#not sure how I want to do the video buffer yet.
	#$manager = multiprocessing.Manager()
	#shared_memory = manager.dict()
	#shared_memory['audio_buffer'] = audio_buffer
	#shared_memory['event_queue'] = event_queue

	p_ml = multiprocessing.Process(target = machine_learning_process.driver, name = 'Machine Learning Process', args=(event_queue,audio_buffer,))
	p_sc = multiprocessing.Process(target = server_communication_process.driver, name = 'Server Communication Process', args = (event_queue,audio_buffer,))
	p_va = multiprocessing.Process(target = alsa_bare_process.driver, name = 'Video / Audio Process', args = (event_queue,audio_buffer,))

	processes = [p_ml,p_sc,p_va]

	for p in processes: p.daemon = True
	for p in processes: p.start()
	#for p in processes: p.join()
	print 'Processes have started successfully.'

	while True:
		#begin looping 
		#print processes[0].is_alive()
		#print 'Updated.'
		x = 10
