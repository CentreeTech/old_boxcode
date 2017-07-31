import requests
import json
import base64
import StringIO
import scipy.io.wavfile
import numpy
import boto
import boto3
import boto.s3
from boto.s3.key import Key
from botocore.client import Config


uuid = '123456789420'
type = 'Crash'

AWS_ACCESS_KEY_ID = 'AKIAIVIY2IPJXLKZUE3A'
AWS_SECRET_ACCESS_KEY = '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'

bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
s3 = boto3.resource(
	's3',
	aws_access_key_id=AWS_ACCESS_KEY_ID,
	aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
	config=Config(signature_version='s3v4')
)


BUCKET_NAME = 'centree-media'

deviceID = 'device_0'
devicePswd = 'day_0'



# assigned to Kaan
def driver(event_queue, audio_buffer):
    print 'Server Communication Process beginning.'
    # queue = shared_memory['event_queue']
    while True:
        event_queue['lock'].acquire()
        if event_queue['data'].empty() is False:
	    print '[SC] Event received.'
            date_time, audio, video_wav, sample_rate, event = event_queue['data'].get()
	    audio = numpy.int16(audio)
	    # now we've got the audio, post in some way
            report_id = report_event(event, deviceID, devicePswd) #this is a blocking call
            audio_wav = StringIO.StringIO()
            scipy.io.wavfile.write(audio_wav, sample_rate, audio)
            send_file_s3(audio_wav, video_wav, report_id, deviceID , devicePswd)  # also this is a blockin call too
            # upload_audio_data(date_time
            print '[SC] Event reported.'
        event_queue['lock'].release()
    return -1


def report_event(event, device_id, password):
    # TODO Handle errors
    # base64.b64encode("device-1213123123:ssuperpass")
    returnJson = {'event': event}
    returnstring = json.dumps(returnJson, sort_keys=True, indent=4, separators=(',', ': '))

    r = requests.post('http://backend.centree.xyz:5000/add_device_event', data=returnstring, headers=headers1)
    parsedJson = json.loads(r.text)

    return parsedJson["report_id"]


def ping(device_id, password):
    print "Will be implemented!"

'''
    file = open('al.mp3', 'rb')
    or
    you can have a virtual file or a file from a variable


    buffer1 = file.read()
    send_file(buffer1, "report-121223", "device_0", "day_1", ".mp3")


'''

def send_file_s3(audio_data, video_data, report_id, device_id, password, audio_format=".wav", video_format = ".h264"):
	#s3_connection = boto.connect_s3()
	#bucket = s3_connection.get_bucket(BUCKET_NAME)
	#key = boto.s3.key.Key(bucket, report_id + audio_format)
	#key.send_file(audio_data)
	s3.Bucket(BUCKET_NAME).put_object(Key=device_id + "/" + report_id+audio_format, Body=audio_data)


#THIS FUNCTION IS DEPRECATED
def send_file(audio_data, video_data, report_id, device_id, password, audio_format=".wav", video_format = ".h264"):
    upload_url = 'http://backend.centree.xyz:5000/upload'

    file_audio = { report_id + audio_format : audio_data}
    file_video = { report_id + video_format : video_data}
    AuthString = "Basic " + str(base64.b64encode(device_id + ":" + password))
	
    headers = {'Authorization': AuthString}

    r = requests.post(upload_url, files=file_audio, headers=headers)
    r = requests.post(upload_url, files=file_video, headers=headers)

    print (r.text)

# def upload_audio_data(name, audio_data, sample_rate, report_id, device_id, password):
# 	AuthString = "Basic" + str(base64.b64encode(device_id + ":" + password))
# 	headers = {'Authorization': AuthString, 'Content-Type': "application/json"}
#
# 	returnJson = {'report_id': report_id}
# 	returnstring = json.dumps(returnJson, sort_keys=True, indent=4, separators=(',', ': '))
#
# 	upload_url = "http://backend.centree.xyz:5000/upload"
# 	audio_payload = {'name': name, 'audio_data': audio_data, 'sample_rate' : sample_rate}
# 	r = requests.post(upload_url, data=json.dumps(audio_payload), headers=headers)
#
#
# def upload_file(file_path, report_id, device_id, password):
#     AuthString = "Basic " + str(base64.b64encode(device_id + ":" + password))
#     headers1 = {'Authorization': AuthString, 'Content-Type': "application/json"}
#
#     returnJson = {'report_id': report_id}
#     returnstring = json.dumps(returnJson, sort_keys=True, indent=4, separators=(',', ': '))
#
#     upload_url = "http://backend.centree.xyz:5000/upload"
#     file = {'file': ('filename', open(file_path, 'rb'))}
#     r = requests.post(upload_url, headers=headers1, data=returnstring, files=file)
