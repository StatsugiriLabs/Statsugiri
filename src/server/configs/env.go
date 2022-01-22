package configs

import (
	"os"

	"github.com/joho/godotenv"
	log "github.com/sirupsen/logrus"
)

// Reads the MongoURI from the environment variable.
func EnvMongoURI() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	return os.Getenv("MONGOURI")
}
