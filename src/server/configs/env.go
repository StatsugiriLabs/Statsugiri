package configs

import (
	"github.com/joho/godotenv"
	log "github.com/sirupsen/logrus"
	"os"
)

func EnvMongoURI() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	return os.Getenv("MONGOURI")
}
