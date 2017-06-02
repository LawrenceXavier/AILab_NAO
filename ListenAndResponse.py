import time
import math
import os
import speech_recognition as sr
import almath as m # python's wrapping of almath
from cleverwrap import CleverWrap
from naoqi import ALProxy

import argparse
from naoqi import ALProxy

def poseInit(robotIP, PORT=9559):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	motionProxy.wakeUp()
	postureProxy.goToPosture("StandInit", 0.5)


def rbRest(robotIP, PORT=9559):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	motionProxy.post.rest()

def goToward(robotIP, PORT=9559):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	motionProxy.wakeUp()
	postureProxy.goToPosture("StandInit", 0.5)
	x = 1.0
	y = 0.0
	theta = 0.0
	frequency = 0.5
	motionProxy.moveToward(x, y, theta, [["Frequency", frequency]])
	time.sleep(3)
	motionProxy.stopMove()

def goBackward(robotIP, PORT=9559):	
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	motionProxy.wakeUp()
	postureProxy.goToPosture("StandInit", 0.5)
	x = -1.0
	y = 0.0
	theta = 0.0
	frequency = 0.5
	motionProxy.moveToward(x, y, theta, [["Frequency", frequency]])
	time.sleep(3)
	motionProxy.stopMove()

def singLonely(robotIP, PORT=9559):
	print "Run here"
	aup = ALProxy("ALAudioPlayer", robotIP, PORT)
	aup.playFile("/home/nao/Akon - Lonely - Lyrics.wav")

def changeCl(naoIP, naoPORT, onOrOff):
	led = ALProxy("ALLeds", naoIP, naoPORT)
	if onOrOff:	 # on
		led.setIntensity("FaceLeds", 1.0)
	else:		# off
		led.setIntensity("FaceLeds", 0.0)

def searchForCommand(s, responseModule, naoIP, naoPORT):
	t = s.split()
	n = len(t)
	i = 0
	no_loop = -1
	while (i < n):
		last_i = i
		if (no_loop != -1):
			no_loop += 1
		if (t[i].find("stop") != -1):
			responseModule.say("Good bye")
			return True
		elif (t[i].find("wake" != -1):
			poseInit(naoIP, naoPORT)
			i += 1
		elif (t[i].find("go") != -1):
			if (i+1 < n):
				if (t[i+1] == "backward" or t[i+1] == "back"):
					goBackward(naoIP, naoPORT)
					i += 1
				else:
					goToward(naoIP, naoPORT)
					if (t[i+1] == "forward" or t[i+1] == "toward" or t[i+1] == "ahead"):
						i += 1
			else:
				goToward(naoIP, naoPORT)
			i += 1
		elif (t[i].find("sing") != -1):
			singLonely(naoIP, naoPORT)
			i += 1
		elif (t[i].find("rest") != -1):
			rbRest(naoIP, naoPORT)
			i += 1
		elif (t[i].find("keep") != -1):
			no_loop = 0
			i += 1
		else:
			i += 1
		if (no_loop >= 1 and no_loop <= 3):
			i = last_i
		elif (no_loop > 3):
			responseModule.say("I am fed up with doing this!")
			no_loop = -1
	return False

def main(naoIP, naoPORT):
	recordModule = ALProxy("ALAudioRecorder", naoIP, naoPORT)
	responseModule = ALProxy('ALTextToSpeech', naoIP, naoPORT)
	recordModule.stopMicrophonesRecording()
	r = sr.Recognizer()
	cb = CleverWrap('CCCloFrKCqTEYteVgk-C70rlxLQ')
	responseModule.say('Hello')
	nb_error = 0
	while (True):	
		# Start recording 		
		print 'Star recording'	
		changeCl(naoIP, naoPORT, True)
		recordModule.startMicrophonesRecording('/home/nao/record.wav', 'wav', 16000, [0, 0, 1, 0])
		time.sleep(3.0)
		changeCl(naoIP, naoPORT, False)
		recordModule.stopMicrophonesRecording()
		print 'Record over'
	
		# Copy record.wav to current folder
		cmd = 'sshpass -p "nao" scp nao@'+naoIP+':record.wav .'
		os.system(cmd)
		
		# Speech To Text
		with sr.AudioFile('record.wav') as source:
			audio = r.record(source)

		try:
			inp = str(r.recognize_google(audio))
			print "Listened: ", inp
			if (inp.find('name') != -1):
				responseModule.say('My name is NAO')
				continue

			# Search for command (if exist); if 'stop' found, then stop
			if (searchForCommand(inp, responseModule, naoIP, naoPORT)):
				break

			# Get response
			try:
				res = cb.say(inp)
			except ValueError:
				res = "I hate you!"
			print "Response: ", res

			# Speak it loud
			responseModule.say(str(res))
			nb_error = 0
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			nb_error += 1
			if (nb_error >= 5):
				responseModule.say("Hello? Are you still there?")
				nb_error = 0
			elif (nb_error >= 3):
				responseModule.say("Hello?")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))

if (__name__ == '__main__'):
	main('192.168.1.18', 9559)
