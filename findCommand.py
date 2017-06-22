import sys
from naoqi import ALProxy
import Actions

def searchForCommand(s, naoIP, naoPORT, lastResponse = "Hello!"):
	"""return 0: nothing ; 1: break ; 2: continue"""
	responseModule = ALProxy("ALTextToSpeech", naoIP, naoPORT)

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
		elif (t[i] == "meet" or t[i] == "met" or t[i] == "see" or t[i] == "saw" or t[i] == "seen"):
	        	if (i+1 >= n):
	                	return 0
		        k = t[i+1]
		        responseModule.say("Hello "+k)
	        	# if (Actions.meetPeople(naoIP, naoPORT, k, responseModule) == 1):
	        	#       return 2
	        	return 0
		elif (t[i] == "wake" or t[i] == "waking" or (i+1 < n and t[i] == "get" and t[i+1] == "up")):
			print "Run here"
	        	Actions.poseInit(naoIP, naoPORT)
	        	i += 1
		elif (t[i] == "go" or t[i] == "going"):
	        	if (i+1 < n):
	                	if (t[i+1] == "backward" or t[i+1] == "back"):
	                        	Actions.goBackward(naoIP, naoPORT)
	                        	i += 1
	                	else:
	                        	Actions.goToward(naoIP, naoPORT)
	                        	if (t[i+1] == "forward" or t[i+1] == "toward" or t[i+1] == "ahead"):
	                                	i += 1
	        	else:
	                	Actions.goToward(naoIP, naoPORT)
	        	i += 1
		elif (t[i] == "sing" or t[i] == "singing"):
	        	Actions.singLonely(naoIP, naoPORT)
	        	i += 1
		        return 2
		elif (t[i] == "rest" or t[i] == "resting"):
	        	Actions.rbRest(naoIP, naoPORT)
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

args = sys.argv
if (len(args) < 5):
	args = args+["Hello"]
r = searchForCommand(args[1], args[2], int(args[3]), args[4])
f = open("nextpart.txt", "w")
f.write(str(r))
f.close()
