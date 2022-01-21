package utils

import (
	"net/http"
	"encoding/json"
)


// TODO: move this to an error.go file
// ERROR RESPONSES
// Generate internal server error response
func CreateInternalServerErrorResponse(rw http.ResponseWriter, err error) {
	rw.WriteHeader(http.StatusInternalServerError)
	json.NewEncoder(rw).Encode(err.Error())
}
