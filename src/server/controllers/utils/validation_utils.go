package utils

import (
	"regexp"
)

const (
	DATE_FORMAT_LEN = 10
)

// Checks provided format is supported.
func ValidFormat(formatToCheck string) bool {
	for _, format := range Formats {
		if formatToCheck == format {
			return true
		}
	}
	return false
}

// Checks if string adheres to valid date format (yyyy-mm-dd)
func ValidDateFormat(dateToCheck string) bool {
	// Validate length of date string
	if len(dateToCheck) != DATE_FORMAT_LEN {
		return false
	}
	// Validate if date string matches yyyy-mm-dd format
	re := regexp.MustCompile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
	return re.MatchString(dateToCheck)
}
