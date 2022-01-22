package errors

import (
	"encoding/json"
	"net/http"
)

// Generates internal server error response.
func CreateInternalServerErrorResponse(rw http.ResponseWriter, err error) {
	rw.WriteHeader(http.StatusInternalServerError)
	json.NewEncoder(rw).Encode(err.Error())
}
