package tests

import (
	"io"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/kelvinkoon/babiri_v2/controllers"
	log "github.com/sirupsen/logrus"

	"github.com/stretchr/testify/assert"
)

// Test health endpoint.
func TestGetHealth(t *testing.T) {
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(controllers.GetHealth())
	handler.ServeHTTP(rr, nil)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), `{"Status":"up and running"}`+"\n")
}
