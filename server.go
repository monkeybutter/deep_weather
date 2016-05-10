package main

import (
	"fmt"
	"log"
	"net/http"
	"os/exec"
)

func mapHandler(w http.ResponseWriter, r *http.Request) {
	r.URL.Query().Get("type")
	mapType := r.URL.Query().Get("type")
	date := r.URL.Query().Get("date")
	param := r.URL.Query().Get("param")
	fmt.Println(mapType, date, param)
	out, err := exec.Command("python", "map_gen.py", date, mapType, param).Output()
	if err != nil {
		log.Println(err)
	}

	w.Write(out)
}

func main() {
	http.HandleFunc("/map", mapHandler)

	fs := http.FileServer(http.Dir("static"))
	http.Handle("/", fs)

	log.Println("Listening...")
	http.ListenAndServe(":3000", nil)
}
