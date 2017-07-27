#from cleverwrap import CleverWrap
import urllib2
import json
from naoqi import ALProxy

url = "http://naofunctions.cloudhub.io/findLesson?query="

def getAnswer(cmd):
	#cb = CleverWrap('CCCloFrKCqTEYteVgk-C70rlxLQ')	
	#res = cb.say(eninp)
	#print "Response: ", res
	print cmd
	cmd = cmd.replace(" ", "%20")
	urlFile = urllib2.urlopen(url+cmd)
	jsonList = json.load(urlFile)
	print jsonList[0]["descLesson"]
	return jsonList[0]["descLesson"]

