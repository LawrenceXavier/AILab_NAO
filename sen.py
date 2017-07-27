from naoqi import ALProxy
import sys

args = sys.argv
tts = ALProxy("ALTextToSpeech", args[1], int(args[2]))
tts.say(args[3])
