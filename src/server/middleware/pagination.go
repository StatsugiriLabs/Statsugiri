package middleware

import (
	"net/http"
	"strconv"
)

const (
	PAGE_QUERY_STR  = "page"
	LIMIT_QUERY_STR = "limit"
	MAX_LIMIT       = 50
)

// Returns the skip and limit given the request.
// Pages are one-indexed.
// Default limit is MAX_LIMIT.
func ParsePagination(rw http.ResponseWriter, r *http.Request) (int, int, error) {
	// Retrieve page and limit query parameters
	pageParam := r.URL.Query().Get(PAGE_QUERY_STR)
	limitParam := r.URL.Query().Get(LIMIT_QUERY_STR)
	// Default page and limit params
	skip := 0
	limit := MAX_LIMIT
	var err error

	// Parse limit query param
	if limitParam != "" {
		limit, err = strconv.Atoi(limitParam)
		if err != nil {
			return 0, MAX_LIMIT, err
		}
		// Verify limit is between 1 and MAX_LIMIT
		if limit > MAX_LIMIT || limit < 1 {
			limit = MAX_LIMIT
		}
	}

	// Parse page query param
	if pageParam != "" {
		skip, err = strconv.Atoi(pageParam)
		if err != nil {
			return 0, MAX_LIMIT, err
		}
		// Default to no skip for first page
		if skip == 1 {
			skip = 0
		} else {
			skip = (skip - 1) * limit
		}
	}

	return skip, limit, nil
}
