import time
import os
import speech_recognition as sr
from cleverwrap import CleverWrap
from naoqi import ALProxy

def getResponse(message):
	if (len(message) <= 3):
		return 'Hello! How are you?'
	elif (len(message) <= 10):
		return 'I am not sure.'
	else:
		return 'I can\'t hear it.'

def main(naoIP, naoPORT):
	recordModule = ALProxy("ALAudioRecorder", naoIP, naoPORT)
	responseModule = ALProxy('ALTextToSpeech', naoIP, naoPORT)
	r = sr.Recognizer()
	cb = CleverWrap('CCCloFrKCqTEYteVgk-C70rlxLQ')

	while (True):	
		# Start recording 
		
		print 'Star recording'	
		recordModule.startMicrophonesRecording('/home/nao/record.wav', 'wav', 16000, [0, 0, 1, 0])
		time.sleep(5.0)
		recordModule.stopMicrophonesRecording()
		print 'Record over'
	
		# Copy record.wav to current folder
		cmd = 'sshpass -p "nao" scp nao@'+naoIP+':record.wav .'
		os.system(cmd)
		
		# Speech To Text
		with sr.AudioFile('record.wav') as source:
			audio = r.record(source)
		inp = r.recognize_google(audio)
		print inp	
		# If find 'stop' in response, stop the program	
		if (str(inp).find('stop') != -1):
			responseModule.say('Good bye')
			break
		
		# Get response
		print inp
		res = cb.say(inp)
		
		# Speak it loud
		responseModule.say(str(res))

if (__name__ == '__main__'):
	main('192.168.1.16', 9559)
