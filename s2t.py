# -*- coding: utf-8 -*-
import sys
import speech_recognition as sr
from translation import bing

def s2t_func():
	r = sr.Recognizer()
	
	with sr.AudioFile("rd.wav") as source:
		audio = r.record(source)
	try:
		inp = r.recognize_google(audio, language="vi-VN")
		
		# Translate into English
		eninp = bing(inp, dst = 'en')
		print "Translated: ", eninp
		
		return eninp
	except sr.UnknownValueError:
		print "Cannot understand!"
	except sr.RequestError as e:
		print "Cannot send request"
	return ""

def s2t_func_vn():
	r = sr.Recognizer()
	with sr.AudioFile("rd.wav") as source:
		audio = r.record(source)
	try:
		inp = r.recognize_google(audio, language="vi-VN")
		print inp.encode("utf8")
		return inp
	except sr.UnknownValueError:
		print "Cannot understand!"
		return "ngồi xuống".decode("utf8")
	except sr.RequestError as e:
		print "Cannot send request!"
	return ""
