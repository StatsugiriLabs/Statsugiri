package controllers

import (
	"encoding/json"
	"net/http"

	"github.com/kelvinkoon/babiri_v2/controllers/utils"
)

// Returns handler for available formats supported.
func GetFormats() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		rw.WriteHeader(http.StatusOK)
		json.NewEncoder(rw).Encode(utils.FormatsRes)
	}
}
