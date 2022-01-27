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

var MongoUri string = getEnv("MONGOURI", "")
var Env string = getEnv("ENV", "DEV")
var DbClusterName string = getEnv("DB_CLUSTER_NAME", "")
var PokemonTeamsSnapshotsCollection string = getEnv("POKEMON_TEAMS_SNAPSHOTS_COLLECTION", "")
var PokemonUsageSnapshotsCollection string = getEnv("POKEMON_USAGE_SNAPSHOTS_COLLECTION", "")
