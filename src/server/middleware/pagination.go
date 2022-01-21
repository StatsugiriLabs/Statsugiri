package middleware

import (
	"net/http"
	"strconv"
)

const (
	PAGE_QUERY_STR  = "page"
	LIMIT_QUERY_STR = "limit"
)

// Return page, limit
// 1 indexed
func ParsePagination(r *http.Request) (int, int) {
	// Retrieve page and limit query parameters
	pageParam := r.URL.Query().Get(PAGE_QUERY_STR)
	limitParam := r.URL.Query().Get(LIMIT_QUERY_STR)

	// Ignore pagination unless both are provided
	if pageParam != "" && limitParam != "" {
		page, _ := strconv.Atoi(pageParam)
		limit, _ := strconv.Atoi(limitParam)

		// Only limit if 1st page requested
		if page == 1 {
			return 0, limit
		}
		return (page - 1) * limit, limit
	}
	return 0, 0
}
