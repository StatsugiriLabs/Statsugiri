package middleware

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/kelvinkoon/babiri_v2/controllers/utils"
)

const (
	PAGE_QUERY_STR  = "page"
	LIMIT_QUERY_STR = "limit"
	START_QUERY_STR = "start"
	END_QUERY_STR   = "end"
)

// Returns the skip and limit given the request.
// Pages are one-indexed.
// Default limit is MAX_LIMIT.
func ParsePagination(rw http.ResponseWriter, r *http.Request, max_limit int) (int, int, error) {
	// Retrieve page and limit query parameters
	pageParam := r.URL.Query().Get(PAGE_QUERY_STR)
	limitParam := r.URL.Query().Get(LIMIT_QUERY_STR)
	// Default page to first page and max limit params
	skip := 0
	limit := max_limit

	// Parse limit query param
	if limitParam != "" {
		rawLimit, err := strconv.Atoi(limitParam)
		if err != nil {
			return 0, max_limit, err
		}
		// Bound limit to MAX_LIMIT if not between 1 and MAX_LIMIT
		if limit > max_limit || limit < 1 {
			limit = max_limit
		} else {
			limit = rawLimit
		}
	}

	// Parse page query param
	if pageParam != "" {
		page, err := strconv.Atoi(pageParam)
		if err != nil {
			return 0, max_limit, err
		}
		// Ensure page is a positive number
		if page <= 0 {
			return 0, max_limit, fmt.Errorf("Page must be a positive number.")
		}
		skip = utils.PageToSkip(page, limit)
	}

	return skip, limit, nil
}

// Returns the start and end of time-series given the request.
func ParseStartAndEnd(rw http.ResponseWriter, r *http.Request) (string, string, error) {
	// Retrieve start and end query parameters
	startParam := r.URL.Query().Get(START_QUERY_STR)
	endParam := r.URL.Query().Get(END_QUERY_STR)
	start := ""
	end := ""

	// Parse start query param
	if startParam != "" {
		if !utils.ValidDateFormat(startParam) {
			return "", "", fmt.Errorf("Start date must follow 'yyyy-mm-dd' format.")
		}
		start = startParam
	}

	// Parse end query param
	if endParam != "" {
		if !utils.ValidDateFormat(endParam) {
			return "", "", fmt.Errorf("End date must follow 'yyyy-mm-dd' format.")
		}
		end = endParam
	}

	return start, end, nil
}
