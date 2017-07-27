import os

naoPATH = "/usr/local/bin:/usr/bin:/bin:/opt/bin:/usr/local/sbin:/usr/sbin:/sbin" 
curPATH = "/home/nao/.local/bin:"+naoPATH

os.environ["PATH"] = naoPATH
print os.getenv("PATH")
os.system("python listen.py")
os.environ["PATH"] = curPATH
