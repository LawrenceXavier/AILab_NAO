from naoqi import ALProxy
import sys
import time
import os

naoPATH = "/usr/local/bin:/usr/bin:/bin:/opt/bin:/usr/local/sbin:/usr/sbin:/sbin" 
curPATH = "/home/nao/.local/bin:"+naoPATH

argv = sys.argv
# argv[1]: naoIP 	argv[2]: naoPORT	argv[3]: filename

pl = ALProxy("ALAudioPlayer", argv[1], int(argv[2]))
filedir = "/home/nao/listenandresponse_VN/update/listenandresponse/"+argv[3]
print filedir
plID = pl.loadFile(filedir)
fLen = pl.getFileLength(plID)
pl.play(plID)
time.sleep(fLen+0.5)
pl.unloadFile(plID)
