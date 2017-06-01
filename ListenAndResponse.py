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

	# Wake up robot
	motionProxy.wakeUp()

	# Send robot to Stand Init
	postureProxy.goToPosture("StandInit", 0.5)


def rbRest(robotIP, PORT=9559):
	# Go to rest position
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	motionProxy.post.rest()

def moveTo(robotIP, PORT=9559):

	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

	# Wake up robot
	motionProxy.wakeUp()

	# Send robot to Stand Init
	postureProxy.goToPosture("StandInit", 0.5)

	#####################
	## Enable arms control by move algorithm
	#####################
	motionProxy.setMoveArmsEnabled(True, True)
	#~ motionProxy.setMoveArmsEnabled(False, False)

	#####################
	## FOOT CONTACT PROTECTION
	#####################
	#~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",False]])
	motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

	#####################
	## get robot position before move
	#####################
	initRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))

	X = 0.3
	Y = 0.0
	Theta = math.pi/2.0
	motionProxy.post.moveTo(X, Y, Theta)
	# wait is useful because with post moveTo is not blocking function
	motionProxy.waitUntilMoveIsFinished()

	#####################
	## get robot position after move
	#####################
	endRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))

	#####################
	## compute and print the robot motion
	#####################
	robotMove = m.pose2DInverse(initRobotPosition)*endRobotPosition
	# return an angle between ]-PI, PI]
	robotMove.theta = m.modulo2PI(robotMove.theta)
#	print "Robot Move:", robotMove

def changeCl(naoIP, naoPORT, onOrOff):
	led = ALProxy("ALLeds", naoIP, naoPORT)
	if onOrOff:	 # on
		led.setIntensity("FaceLeds", 1.0)
	else:		# off
		led.setIntensity("FaceLeds", 0.0)

def searchForCommand(s, responseModule, naoIP, naoPORT):
	t = s.split()
	for x in t:
		if (x.find('stop') != -1):
			responseModule.say('Good bye')
			return True
		elif (x.find('wake') != -1):
			poseInit(naoIP, naoPORT)
		elif (x.find('go') != -1):
			moveTo(naoIP, naoPORT)
		elif (x.find('rest') != -1):
			rbRest(naoIP, naoPORT)
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

			if (inp.find('name') != -1):
				res = responseModule.say('My name is NAO')
				continue

			# Search for command (if exist); if 'stop' found, then stop
			if (searchForCommand(inp, responseModule, naoIP, naoPORT)):
				break

			# Get response
			res = cb.say(inp)

			# Speak it loud
			responseModule.say(str(res))
			nb_error = 0
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			nb_error += 1
			if (nb_error >= 5):
				responseModule.say("Hello? Are you still there?")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))

if (__name__ == '__main__'):
	main('192.168.1.12', 9559)
