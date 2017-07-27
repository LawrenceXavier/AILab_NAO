import os
import s2t
import getResponse
import svn

naoPATH = "/usr/local/bin:/usr/bin:/bin:/opt/bin:/usr/local/sbin:/usr/sbin:/sbin" 
curPATH = "/home/nao/.local/bin:"+naoPATH

last_sentence = "Hello!"

try:
	f = open("last_sentence.txt", "r")
	last_sentence = f.readline()
	f.close()
except IOError:
	print "Cannot open file..."
else:
	print "Error while reading..."
	f.close()

# S2T: from input (VN) to text (EN)
os.environ["PATH"] = curPATH	
eninp = s2t.s2t_func()

# Find command in the text and act
os.environ["PATH"] = naoPATH
os.system("python findCommand.py \"%s\" \"nao.local\" 9559 \"%s\"" % (eninp, last_sentence))

# Get static response
res = getResponse.getAnswer(eninp)

# Speak it out
os.system("python sen.py \"nao.local\" 9559 \"%s\"" % (res))

os.environ["PATH"] = curPATH

# Translate response into Vietnamese
# svn.speakVN(res) 

f = open("last_sentence.txt", "w")
f.write(res+"\n")
f.close()

f = open("nextpart.txt", "r")
r = int(f.readline())
f.close()
if (r != 0):
	exit(0)

# os.environ["PATH"] = naoPATH
# os.system("python say.py \"%s\" \"nao.local\" 9559" % (res))

