package utils

import (
	"github.com/kelvinkoon/babiri_v2/models"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

// Generates a aggregation pipeline for team queries.
// Prepends team unwinding and reverse chronological sorting.
// Includes Pokémon query if parameter provided.
func MakeTeamQueryPipeline(pokemon string, intermediateStages []bson.M) []bson.M {
	// Unwind team replay information
	unwindTeamStage := bson.M{"$unwind": "$Teams"}
	// Sort teams by rating
	sortByRatingStage := bson.M{"$sort": bson.M{"Rating": -1}}

	// Initialize pipeline stages
	pipelineStages := []bson.M{unwindTeamStage, sortByRatingStage}
	// Add intermediate aggregation stages
	pipelineStages = append(pipelineStages, intermediateStages...)

	// Match all teams with Pokémon if provided
	if pokemon != "" {
		matchByPokemonStage := bson.M{
			"$match": bson.M{
				"Teams.PokemonRoster": pokemon,
			},
		}
		pipelineStages = append(pipelineStages, matchByPokemonStage)
	}

	// Group Pokémon team snapshots before unwind
	groupTeamSnapshotsStage := bson.M{
		"$group": bson.M{
			"_id":      "$_id",
			"Date":     bson.M{"$first": "$Date"},
			"FormatId": bson.M{"$first": "$FormatId"},
			"Teams":    bson.M{"$push": "$Teams"},
		},
	}
	pipelineStages = append(pipelineStages, groupTeamSnapshotsStage)

	// Sort team snapshots in reverse chronological order and then by format
	sortByDateandFormatStage := bson.M{"$sort": bson.D{
		primitive.E{Key: "Date", Value: -1},
		primitive.E{Key: "FormatId", Value: -1},
	}}
	pipelineStages = append(pipelineStages, sortByDateandFormatStage)

	return pipelineStages
}

// Generates a aggregation pipeline for usage queries.
func MakeUsageQueryPipeline(usageType UsageType, intermediateStages []bson.M) []bson.M {
	// Sort team snapshots in reverse chronological order
	sortByDateandFormatStage := bson.M{"$sort": bson.D{
		primitive.E{Key: "Date", Value: -1},
		primitive.E{Key: "FormatId", Value: -1},
	}}

	// Extract necessary fields
	groupUsageResponseStage := bson.M{
		"$project": bson.M{
			"_id":                       false,
			"Date":                      1,
			"FormatId":                  1,
			"PokemonUsage":              1,
			"PokemonPartnerUsage":       1,
			"PokemonAverageRatingUsage": 1,
		},
	}

	// Initialize pipeline stages
	pipelineStages := []bson.M{sortByDateandFormatStage, groupUsageResponseStage}
	// Add intermediate aggregation stages
	pipelineStages = append(pipelineStages, intermediateStages...)

	// // Group Pokémon usage snapshots before unwind
	// groupTeamSnapshotsStage := bson.M{
	// 	"$group": bson.M{
	// 		"_id":      "$_id",
	// 		"Date":     bson.M{"$first": "$Date"},
	// 		"FormatId": bson.M{"$first": "$FormatId"},
	// 		"PokemonPartnerUsages":    bson.M{"$push": "$PokemonPartnerUsages"},
	// 	},
	// }
	// pipelineStages = append(pipelineStages, groupTeamSnapshotsStage)

	return pipelineStages
}

func MakeTimeSeriesUsageQueryPipeline(pokemon string, intermediateStages []bson.D) []bson.D {
	// Sort usage in reverse chronological order
	// TODO: Make sorting by format as well
	sortByDateStage := bson.D{
		primitive.E{
			Key: "$sort", Value: bson.D{
				primitive.E{
					Key: "Date", Value: -1,
				},
			},
		},
	}

	// Extract necessary fields
	pokemonKey := "PokemonUsage." + pokemon
	groupUsageResponseStage := bson.D{
		primitive.E{
			Key: "$project", Value: bson.D{
				primitive.E{
					Key: "Date", Value: 1,
				},
				primitive.E{
					Key: "FormatId", Value: 1,
				},
				primitive.E{
					Key: "_id", Value: 0,
				},
				primitive.E{
					Key: pokemonKey, Value: 1,
				},
			},
		},
	}

	// Initialize pipeline stages
	pipelineStages := []bson.D{sortByDateStage, groupUsageResponseStage}
	// Add intermediate aggregation stages
	pipelineStages = append(pipelineStages, intermediateStages...)

	return pipelineStages
}

// Generates cache composite key from request type, Pokémon, and pagination options.
func MakeCompositeKey(params ...string) string {
	// Generate composite key
	var composite_key string
	for _, param := range params {
		composite_key += param
	}
	return composite_key
}

// Paginate team snapshot aggregation results through slicing.
// TODO: Handle 0 page index
func SliceTeamSnapshots(snapshots []models.PokemonTeamsSnapshot, skip int, size int) []models.PokemonTeamsSnapshot {
	// Limit skip to length of results
	if skip > len(snapshots) {
		skip = len(snapshots)
	}

	end := skip + size

	// Limit end to length of results
	if end > len(snapshots) {
		end = len(snapshots)
	}

	return snapshots[skip:end]
}

// Paginate usage snapshot aggregation results through slicing.
func SliceUsageSnapshots(snapshots []models.PokemonUsageSnapshot, skip int, size int) []models.PokemonUsageSnapshot {
	// Limit skip to length of results
	if skip > len(snapshots) {
		skip = len(snapshots)
	}

	end := skip + size

	// Limit end to length of results
	if end > len(snapshots) {
		end = len(snapshots)
	}

	return snapshots[skip:end]
}
