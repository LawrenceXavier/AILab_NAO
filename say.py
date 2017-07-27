from naoqi import ALProxy
import sys
import time

argv = sys.argv
#tts = ALProxy("ALTextToSpeech", argv[2], int(argv[3]))
#tts.say(argv[1])

pl = ALProxy("ALAudioPlayer", argv[2], int(argv[3]))
plID = pl.loadFile("/home/nao/listenandresponse_VN/update/listenandresponse/res.mp3")
fLen = pl.getFileLength(plID)
time.sleep(fLen+0.5)
pl.play(plID)

