package controllers

import (
	"encoding/json"
	"net/http"
)

type healthCheckResponse struct {
	Status string `json:"status"`
}

// Returns handler for backend heartbeat.
func GetHealth() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		rw.WriteHeader(http.StatusOK)
		json.NewEncoder(rw).Encode(healthCheckResponse{Status: "up and running"})
	}
}
