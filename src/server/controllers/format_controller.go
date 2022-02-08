package controllers

import (
	"encoding/json"
	"net/http"

	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	"github.com/kelvinkoon/babiri_v2/responses"
)

// Returns handler for available formats supported.
func GetFormats() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		rw.WriteHeader(http.StatusOK)
		json.NewEncoder(rw).Encode(responses.FormatResponse{Formats: utils.Formats})
	}
}
