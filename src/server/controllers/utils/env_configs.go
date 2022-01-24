package utils

import (
	"os"
)

var MongoUri string = os.Getenv("MONGOURI")
var Env string = os.Getenv("ENV")
var DbClusterName string = os.Getenv("DB_CLUSTER_NAME")
var PokemonTeamsSnapshotsCollection string = os.Getenv("POKEMON_TEAMS_SNAPSHOTS_COLLECTION")
var PokemonUsageSnapshotsCollection string = os.Getenv("POKEMON_USAGE_SNAPSHOTS_COLLECTION")
