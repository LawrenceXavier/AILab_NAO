import sys
import speech_recognition as sr
from translation import bing

def s2t_func():
	r = sr.Recognizer()
	
	with sr.AudioFile("rd.wav") as source:
		audio = r.record(source)
	
	try:
		inp = r.recognize_google(audio, language="vi-VN")
		
		eninp = bing(inp, dst = 'en')
		print "Translated: ", eninp
		
		return eninp
	except sr.UnknownValueError:
		print "Cannot understand!"
	except sr.RequestError as e:
		print "Cannot send request"
	return ""
