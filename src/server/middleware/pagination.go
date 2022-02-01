package middleware

import (
	"net/http"
	"strconv"
)

const (
	PAGE_QUERY_STR  = "page"
	LIMIT_QUERY_STR = "limit"
)

// Returns the skip and limit given the request.
// Pages are one-indexed.
// Default limit is MAX_LIMIT.
func ParsePagination(rw http.ResponseWriter, r *http.Request, max_limit int) (int, int, error) {
	// Retrieve page and limit query parameters
	pageParam := r.URL.Query().Get(PAGE_QUERY_STR)
	limitParam := r.URL.Query().Get(LIMIT_QUERY_STR)
	// Default page and limit params
	skip := 0
	limit := max_limit
	var err error

	// Parse limit query param
	if limitParam != "" {
		limit, err = strconv.Atoi(limitParam)
		if err != nil {
			return 0, max_limit, err
		}
		// Verify limit is between 1 and MAX_LIMIT
		if limit > max_limit || limit < 1 {
			limit = max_limit
		}
	}

	// Parse page query param
	if pageParam != "" {
		skip, err = strconv.Atoi(pageParam)
		if err != nil {
			return 0, max_limit, err
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
