from naoqi import ALProxy
import sys

argv = sys.argv
tts = ALProxy("ALTextToSpeech", argv[2], int(argv[3]))
tts.say(argv[1])

