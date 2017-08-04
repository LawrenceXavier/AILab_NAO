from translation import bing
from cleverwrap import CleverWrap

def getBotResponse(vninp):
	# Translate into English
	eninp = bing(vninp, dst="en")

	# Clever chatbot
	cb = CleverWrap("CCCloFrKCqTEYteVgk-C70rlxLQ")
	enres = cb.say(eninp)
	
	# Translate response into Vietnamese
	vnres = bing(enres, dst="vi")
	vnres = vnres.encode("utf8")
	
	return vnres
