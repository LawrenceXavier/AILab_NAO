from gtts import gTTS
import svn
import json
import requests
import urllib2

url = "http://naofunctions.cloudhub.io/getAllLesson"

if (__name__ == "__main__"):
	print "Loading data..."
	urlFile = urllib2.urlopen(url)
	jsonList = json.load(urlFile)
	for item in jsonList:
		res = item["descLesson"]
		res = res.encode("utf8")
		print res
		svn.speakVN(res, item["doFunction"]+".mp3")
