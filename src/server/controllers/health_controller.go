package controllers

import (
	"encoding/json"
	"net/http"

	"github.com/kelvinkoon/babiri_v2/responses"
)

// Returns handler for backend heartbeat.
func GetHealth() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		rw.WriteHeader(http.StatusOK)
		json.NewEncoder(rw).Encode(responses.HealthResponse{Status: "up and running"})
	}
}
