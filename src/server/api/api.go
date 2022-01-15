package api

import (
	"net/http"
	"strconv"
	"time"
	mux "github.com/gorilla/mux"
	log "github.com/sirupsen/logrus"
)

const READ_TIMEOUT_DURATION = 30
const WRITE_TIMEOUT_DURATION = 30

func Serve(port int) {
	r := mux.NewRouter()
	r.HandleFunc("/health", healthCheckFunc).Methods("GET")

	http.Handle("/", r)

	server := newServer(":" + strconv.Itoa(port), r)
	log.Infof("Server is running on Port %s", strconv.Itoa(port))

	err := server.ListenAndServe()
	if err != nil {
		log.Fatal(err)
	}
}

func newServer(addr string, router http.Handler) *http.Server {
	return &http.Server{
		Addr:         addr,
		Handler:      router,
		ReadTimeout:  time.Second * READ_TIMEOUT_DURATION,
		WriteTimeout: time.Second * WRITE_TIMEOUT_DURATION,
	}
}
