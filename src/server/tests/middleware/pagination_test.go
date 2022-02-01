package tests

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/kelvinkoon/babiri_v2/middleware"
	"github.com/stretchr/testify/assert"
)

// Test parsing pagination for first page with limit.
func TestParsePaginationFirstPage(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	rr := httptest.NewRecorder()
	skip, limit, err := middleware.ParsePagination(rr, req, 50)

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)

	assert.Nil(t, err)
	// Check no skips for first page
	assert.Equal(t, skip, 0)
	assert.Equal(t, limit, 5)
}

// Test parsing pagination for arbitrary page (ie. 2nd page).
func TestParsePaginationSkipPage(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "2")
	q.Add("limit", "3")
	req.URL.RawQuery = q.Encode()

	rr := httptest.NewRecorder()
	skip, limit, err := middleware.ParsePagination(rr, req, 50)

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)

	assert.Nil(t, err)
	// Check skip adheres to (skip - 1) * limit formula
	assert.Equal(t, skip, 3)
	assert.Equal(t, limit, 3)
}

// Test parsing pagination when no params given.
func TestParsePaginationNoParams(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rr := httptest.NewRecorder()
	skip, limit, err := middleware.ParsePagination(rr, req, 50)

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)

	assert.Nil(t, err)
	// Check skip and limit are default
	assert.Equal(t, skip, 0)
	assert.Equal(t, limit, 50)
}
