package utils

// Convert from page number to number of items to skip given page and limit.
func PageToSkip(page int, limit int) int {
	// Default to no skip for first page
	if page == 1 {
		return 0
	}
	return (page - 1) * limit
}

// Convert from number of items to skip to page number given skip and limit.
func SkipToPage(skip int, limit int) int {
	// No skip defaults to first page
	if skip == 0 {
		return 1
	}
	return skip/limit + 1
}
