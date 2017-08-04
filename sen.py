from naoqi import ALProxy
import sys

def speakOut(naoIP, naoPORT, utt):
	tts = ALProxy("ALTextToSpeech", naoIP, naoPORT)
	tts.say(utt)

# args = sys.argv
# tts = ALProxy("ALTextToSpeech", args[1], int(args[2]))
# tts.say(args[3])
