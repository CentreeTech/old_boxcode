
from subprocess import call
from flask import Flask

#call(["ls", "-l"])

class Network_Handler():

	@staticmethod
	def start_access_point():
		call["sudo hotspotd start"]

	@staticmethod
	def stop_access_point():
		call["sudo hotspotd stop"]

	@staticmethod
	def connect_to_wifi(ssid, password):
		return ("todo")


class WifiSetupServer():

	__init__(self):
		self.app = Flask(__name__)

		@app.route("/")
		def hello():
    	return "Hello World!"