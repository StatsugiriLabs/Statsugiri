package tests

import (
	"fmt"
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

// Test parsing pagination when invalid page given.
func TestParsePaginationInvalidPage(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "0")
	req.URL.RawQuery = q.Encode()

	rr := httptest.NewRecorder()
	_, _, err := middleware.ParsePagination(rr, req, 50)

	assert.Equal(t, err, fmt.Errorf("Page must be a positive number."))
}

// Test parsing start/end happy path.
func TestParseStartAndEndHappyPath(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("start", "2022-01-01")
	q.Add("end", "2022-01-31")
	req.URL.RawQuery = q.Encode()

	rr := httptest.NewRecorder()
	start, end, err := middleware.ParseStartAndEnd(rr, req)

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)

	assert.Nil(t, err)
	// Check no skips for first page
	assert.Equal(t, start, "2022-01-01")
	assert.Equal(t, end, "2022-01-31")
}

// Test start/end when no params given.
func TestParseStartAndEndNoParams(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rr := httptest.NewRecorder()
	start, end, err := middleware.ParseStartAndEnd(rr, req)

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)

	assert.Nil(t, err)
	// Check start and end are not populated
	assert.Equal(t, start, "")
	assert.Equal(t, end, "")
}

// Test parsing start/end when invalid start given.
func TestParseStartAndEndInvalidStart(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("start", "invalid_start")
	req.URL.RawQuery = q.Encode()

	rr := httptest.NewRecorder()
	_, _, err := middleware.ParseStartAndEnd(rr, req)

	assert.Equal(t, err, fmt.Errorf("Start date must follow 'yyyy-mm-dd' format."))
}

// Test parsing start/end when invalid end given.
func TestParseStartAndEndInvalidEnd(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("end", "invalid_end")
	req.URL.RawQuery = q.Encode()

	rr := httptest.NewRecorder()
	_, _, err := middleware.ParseStartAndEnd(rr, req)

	assert.Equal(t, err, fmt.Errorf("End date must follow 'yyyy-mm-dd' format."))
}
