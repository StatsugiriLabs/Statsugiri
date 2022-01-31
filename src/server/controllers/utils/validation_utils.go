package utils

// Checks provided format is supported.
func ValidFormat(formatToCheck string) bool {
	for _, format := range Formats {
		if formatToCheck == format {
			return true
		}
	}
	return false
}
