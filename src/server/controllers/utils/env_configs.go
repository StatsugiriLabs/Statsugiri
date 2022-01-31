package utils

import (
	"os"
)

func getEnv(key, fallback string) string {
	value, exists := os.LookupEnv(key)
	if !exists {
		value = fallback
	}
	return value
}

var MongoUri string = getEnv("MONGOURI", "mongodb://localhost:27017") // Default to local on Port 27017
var Env string = getEnv("ENV", "DEV")                                 // Default to DEV environment
