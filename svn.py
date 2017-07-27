from gtts import gTTS
from translation import bing

def speakVN(res):	
	print res
	vnres = bing(res, dst="vi")
	print vnres.encode("utf8")
	tts = gTTS(text=vnres.encode('utf8'), lang="vi", slow=False)
	tts.save("res.mp3")
