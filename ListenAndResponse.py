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
	aup = ALProxy("ALAudioPlayer", robotIP, PORT)
	aup.playFile("/home/nao/Akon - Lonely - Lyrics.wav", 0.3, 0.0)
	time.sleep(8.0)
	aup.stopAll()

def meetPeople(robotIP, PORT, sbName, responseModule):
	if (not sbName):
		return
	fdProxy = ALProxy("ALFaceDetection", robotIP, PORT)
	memProxy = ALProxy("ALMemory", robotIP, PORT)
	
	fdProxy.setRecognitionEnabled(True)
	fdProxy.subscribe("Meet_new_friend", 500, 0.0)
	time.sleep(0.5)
	val = memProxy.getData("FaceDetected")
	if (val and isinstance(val, list) and len(val) >= 2):
		timeStamp = val[0]
		faceInfoArray = val[1]
		try:
			faceInfo = faceInfoArray[0]	# Just recognize the first face
			faceShapeInfo = faceInfo[0]
			faceExtraInfo = faceInfo[1]
			if (not (faceExtraInfo and faceExtraInfo[2])):
				responseModule.say("Please keep this for five seconds!")
				faceProxy.learnFace(sbName)
				responseModule.say("Now I've remembered you, "+sbName)
			else:
				responseModule.say("Hello, "+faceExtraInfo[2])
		except Exception, e:
			print "Error: "
			print str(e)
			return 1
	fdProxy.unsubscribe("Meet_new_friend")
	return 0

def changeCl(naoIP, naoPORT, onOrOff):
	led = ALProxy("ALLeds", naoIP, naoPORT)
	if onOrOff:	 # on
		led.setIntensity("FaceLeds", 1.0)
	else:		# off
		led.setIntensity("FaceLeds", 0.0)

def searchForCommand(s, responseModule, naoIP, naoPORT, lastResponse = "Hello!"):	# return 0: nothing ; 1: break ; 2: continue
	if (s.find("name") != -1):
		responseModule.say("My name is NAO!")
		return 2
	t = s.split()
	n = len(t)
	i = 0
	no_loop = -1
	while (i < n):
		last_i = i
		if (no_loop != -1):
			no_loop += 1
		if (t[i] == "stop" or t[i] == "stopped" or t[i] == "stopping"):
			responseModule.say("Good bye!")
			return 1
		elif (t[i] == "say" or t[i] == "said" or t[i] == "saying"):	
			k = " ".join(t[j] for j in range(i+1, n))
			responseModule.say(k)
			return 2
		elif (t[i] == "repeat" or t[i] == "repeating" or t[i] == "repeated"):
			responseModule.say(lastResponse)
			return 2
		elif (t[i] == "meet" or t[i] == "met"):
			k = " ".join(t[j] for j in range(i+1, n))
			if (meetPeople(naoIP, naoPORT, k, responseModule) == 1):
				return 2
			return 0
		elif (t[i] == "wake" or t[i] == "waking"):
			poseInit(naoIP, naoPORT)
			i += 1
		elif (t[i] == "go" or t[i] == "going"):
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
		elif (t[i] == "sing" or t[i] == "singing"):
			singLonely(naoIP, naoPORT)
			i += 1
			return 2

		elif (t[i] == "rest" or t[i] == "resting"):
			rbRest(naoIP, naoPORT)
			i += 1
		elif (t[i] == "keep" or t[i] == "keeping"):
			no_loop = 0
			i += 1
		else:
			i += 1
		if (no_loop >= 1 and no_loop <= 3):
			i = last_i
		elif (no_loop > 3):
			responseModule.say("I am fed up with this!")
			no_loop = -1
	return 0

def main(naoIP, naoPORT):
	recordModule = ALProxy("ALAudioRecorder", naoIP, naoPORT)
	responseModule = ALProxy("ALTextToSpeech", naoIP, naoPORT)
	recordModule.stopMicrophonesRecording()
	r = sr.Recognizer()
	cb = CleverWrap('CCCloFrKCqTEYteVgk-C70rlxLQ')
	responseModule.say("Hello!")
	nb_error = 0
	last_response = "Hello!"
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
			c = searchForCommand(inp, responseModule, naoIP, naoPORT, last_response)
			if (c == 1):
				break
			elif (c == 2):
				continue

			# Get response
			try:
				res = cb.say(inp)
			except ValueError:
				res = "I hate you!"
			print "Response: ", res

			# Speak it loud
			responseModule.say(str(res))
			last_response = str(res)
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
	main('192.168.1.24', 9559)
