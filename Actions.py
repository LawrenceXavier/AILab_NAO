import time
import math
import os
import almath as m # python's wrapping of almath
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
        aup.playFile("/home/nao/listenandresponse/Akon - Lonely - Lyrics.wav", 0.3, 0.0)
        time.sleep(8.0)
        aup.stopAll()

def meetPeople(robotIP, PORT, sbName, responseModule):
        if (not sbName):
                return
        print sbName, type(sbName)
        fdProxy = ALProxy("ALFaceDetection", robotIP, PORT)
        fdProxy.setRecognitionEnabled(True)
        fdProxy.subscribe("Meet_new_friend", 500, 0.0)

        memProxy = ALProxy("ALMemory", robotIP, PORT)
	for i in range(5):
                time.sleep(0.5)
                val = memProxy.getData("FaceDetected")
                if (val and isinstance(val, list) and len(val) >= 2):
                        timeStamp = val[0]
                        faceInfoArray = val[1]

                        try:
                                faceInfo = faceInfoArray[0]     # Just recognize the first face
                                faceShapeInfo = faceInfo[0]
                                faceExtraInfo = faceInfo[1]
                                if (not (faceExtraInfo and faceExtraInfo[2])):
                                        responseModule.say("Please keep this for five seconds!")
                                        fdProxy.learnFace(str(sbName))
                                        time.sleep(5.0)
                                        responseModule.say("Now I've remembered you, "+sbName)
                                else:
                                        responseModule.say("Hello, "+faceExtraInfo[2])
                        except Exception, e:
                                print "Error: "
                                print str(e)
                                return 1
			break
                else:
                        print "No face found"
        fdProxy.unsubscribe("Meet_new_friend")
        return 0

