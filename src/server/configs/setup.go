package configs

import (
    "context"
    "time"
	log "github.com/sirupsen/logrus"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

const CONN_TIMEOUT = 10

func ConnectDB() *mongo.Client  {
	// Configure new client
    client, err := mongo.NewClient(options.Client().ApplyURI(EnvMongoURI()))
    if err != nil {
        log.Fatal(err)
    }
  
	// Define connection timeout
    ctx, cancel := context.WithTimeout(context.Background(), CONN_TIMEOUT*time.Second)
	defer cancel()
    err = client.Connect(ctx)
    if err != nil {
        log.Fatal(err)
    }

    // Ping DB to verify connection
    err = client.Ping(ctx, nil)
    if err != nil {
        log.Fatal(err)
    }

	log.Infof("Connected to MongoDB instance")
    return client
}

// Client instance
var DB *mongo.Client = ConnectDB()

// Getting database collections
func GetCollection(client *mongo.Client, collectionName string) *mongo.Collection {
	// TODO: Make this an env var
    collection := client.Database("babiri-dev-cluster").Collection(collectionName)
    return collection
}
