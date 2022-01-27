package configs

import (
	"context"
	"time"

	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	log "github.com/sirupsen/logrus"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const (
	CONN_TIMEOUT = 10
)

// Connects to the MongoDB database.
// Returns a Mongo client for accessing the instance.
func ConnectDB() *mongo.Client {
	// Configure new client
	client, err := mongo.NewClient(options.Client().ApplyURI(utils.MongoUri))
	if err != nil {
		log.Fatal(err)
	}

	// Define connection timeout
	ctx, cancel := context.WithTimeout(context.Background(), CONN_TIMEOUT*time.Second)
	defer cancel()

	// Connect to DB
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

// DB Client instance
var DB *mongo.Client = ConnectDB()
var TeamCollection *mongo.Collection = GetCollection(DB, utils.PokemonTeamSnapshotsCollectionName)

// Returns a specified database collection
func GetCollection(client *mongo.Client, collectionName string) *mongo.Collection {
	collection := client.Database(utils.DbClusterName).Collection(collectionName)
	return collection
}
