package tests

import (
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"

	internal_err "github.com/kelvinkoon/babiri_v2/errors"
	"github.com/stretchr/testify/assert"
)

// Test creating an internal server error.
func TestCreateInternalServerErrorResponse(t *testing.T) {
	rr := httptest.NewRecorder()
	err := errors.New("")
	internal_err.CreateInternalServerErrorResponse(rr, err)

	// Check status code
	assert.Equal(t, rr.Code, http.StatusInternalServerError)
}

// Test creating a bad request server error.
func TestCreateBadRequestErrorResponse(t *testing.T) {
	rr := httptest.NewRecorder()
	err := errors.New("")
	internal_err.CreateBadRequestErrorResponse(rr, err)

	// Check status code
	assert.Equal(t, rr.Code, http.StatusBadRequest)
}
