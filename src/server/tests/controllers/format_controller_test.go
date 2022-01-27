package tests

import (
	"io"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/kelvinkoon/babiri_v2/controllers"
	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	log "github.com/sirupsen/logrus"

	"github.com/stretchr/testify/assert"
)

// Construct expected format response as string
func getExpectedFormatResponse() string {
	formats := utils.Formats
	responseBody := `{"formats":[`
	for i, format := range formats {
		responseBody += "\"" + format + "\""
		// Ignore comma for last format item
		if i != len(formats)-1 {
			responseBody += ","
		}
	}
	// json/encoding adds an extra newline character
	responseBody += `]}` + "\n"
	return responseBody
}

// Test format retrieval handler.
func TestGetFormats(t *testing.T) {
	expectedRes := getExpectedFormatResponse()
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(controllers.GetFormats())
	handler.ServeHTTP(rr, nil)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), expectedRes)
}
