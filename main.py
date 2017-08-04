import os

naoPATH = "/usr/local/bin:/usr/bin:/bin:/opt/bin:/usr/local/sbin:/usr/sbin:/sbin" 
curPATH = "/home/nao/.local/bin:"+naoPATH

# Load all static responses
os.environ["PATH"] = curPATH
os.system("python speakAll.py")

os.environ["PATH"] = naoPATH
print os.getenv("PATH")
os.system("python listen.py")
os.environ["PATH"] = curPATH
