import os
import s2t
import getResponse

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

os.environ["PATH"] = curPATH	
eninp = s2t.s2t_func()

os.environ["PATH"] = naoPATH
os.system("python findCommand.py \"%s\" \"nao.local\" 9559 \"%s\"" % (eninp, last_sentence))

os.environ["PATH"] = curPATH

res = getResponse.getAnswer(eninp)

f = open("last_sentence.txt", "w")
f.write(res)
f.close()

f = open("nextpart.txt", "r")
r = int(f.readline())
f.close()
if (r != 0):
	exit(0)

os.environ["PATH"] = naoPATH
os.system("python say.py \"%s\" \"nao.local\" 9559" % (res))

