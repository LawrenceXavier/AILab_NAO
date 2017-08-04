from gtts import gTTS
from translation import bing
from gtts import gTTS

def translateToVN(res):
	return bing(res, dst="vi")

def speakVN(res, filename="res.mp3"):
	print "Text To Speech:", res
	tts = gTTS(res, lang="vi", slow=False)
	tts.save(filename)
