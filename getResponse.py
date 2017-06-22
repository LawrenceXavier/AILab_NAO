from cleverwrap import CleverWrap

def getAnswer(eninp):
	cb = CleverWrap('CCCloFrKCqTEYteVgk-C70rlxLQ')	
	res = cb.say(eninp)
	print "Response: ", res
	return res
