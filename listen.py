#!/usr/bin/python

from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker
import time
import os
import sys

naoPATH = "/usr/local/bin:/usr/bin:/bin:/opt/bin:/usr/local/sbin:/usr/sbin:/sbin" 
curPATH = "/home/nao/.local/bin:"+naoPATH

listenmodule = None
memory = None

class ListenModule(ALModule):
	""" A module able to record sound 
		whenever it is detected
	"""
	def __init__(self, name):
		ALModule.__init__(self, name)
		self.rd = ALProxy("ALAudioRecorder")
		global memory
		memory = ALProxy("ALMemory")
		memory.subscribeToEvent("SoundDetected", "listenmodule", "recordText")

	def recordText(self, *_args):
		memory.unsubscribeToEvent("SoundDetected", "listenmodule")
		
		print "Start recording..."
		self.rd.stopMicrophonesRecording()
		self.rd.startMicrophonesRecording("/home/nao/listenandresponse_VN/update/listenandresponse/rd.wav", "wav", 16000, [0, 0, 1, 0])
		time.sleep(3.0)
		self.rd.stopMicrophonesRecording()
		print "Stop recording..."
		
		os.environ["PATH"] = curPATH
		os.system("python afterListening.py")
		os.environ["PATH"] = naoPATH
		
		f = open("nextpart.txt", "r")
		r = int(f.readline())
		f.close()
		if (r == 1):
			sys.exit(0)
		
		memory.subscribeToEvent("SoundDetected", "listenmodule", "recordText")

def main():	
	mybroker = ALBroker("mybroker", "0.0.0.0", 9999, "nao.local", 9559)
	
	try:
		global listenmodule 
		listenmodule = ListenModule("listenmodule")
	except Exception, e:
		print "error"
		print str(e)
		sys.exit(1)
	
	try:
		while (True):
			time.sleep(1.0)
	except KeyboardInterrupt:
		print "Stop listening"
		mybroker.shutdown()
		sys.exit(0)

if (__name__ == "__main__"):
	main()
