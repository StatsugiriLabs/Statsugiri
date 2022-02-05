package utils

import (
	"github.com/kelvinkoon/babiri_v2/models"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

var pokemonUsageProjectField primitive.E = primitive.E{
	Key: "PokemonUsage", Value: 1,
}
var pokemonPartnerUsageProjectField primitive.E = primitive.E{
	Key: "PokemonPartnerUsage", Value: 1,
}
var pokemonAverageRatingUsageProjectField primitive.E = primitive.E{
	Key: "PokemonAverageRatingUsage", Value: 1,
}

// Generates a aggregation pipeline for team queries.
// Prepends team unwinding and reverse chronological sorting.
// Includes Pokémon query if parameter provided.
func MakeTeamQueryPipeline(pokemon string, intermediateStages []bson.M) []bson.M {
	// Unwind team replay information
	unwindTeamStage := bson.M{"$unwind": "$Teams"}
	// Sort teams by rating
	sortByRatingStage := bson.M{"$sort": bson.M{"Rating": -1}}

	// // Initialize pipeline stages
	pipelineStages := []bson.M{unwindTeamStage, sortByRatingStage}
	// // Add intermediate aggregation stages
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

	// Sort team snapshots in reverse chronological order
	sortByDateStage := bson.M{"$sort": bson.M{"Date": -1}}
	pipelineStages = append(pipelineStages, sortByDateStage)

	return pipelineStages
}

// Generates a aggregation pipeline for usage queries.
// Prepends team unwinding and reverse chronological sorting.
func MakeUsageQueryPipeline(usageType UsageType, intermediateStages []bson.D) []bson.D {
	// Assign usage field for project stage based on usage type
	var usageProjectField primitive.E
	switch usageType {
	case Usage:
		usageProjectField = pokemonUsageProjectField
	case PartnerUsage:
		usageProjectField = pokemonPartnerUsageProjectField
	case RatingUsage:
		usageProjectField = pokemonAverageRatingUsageProjectField
	default:
		usageProjectField = pokemonUsageProjectField
	}

	// Sort teams by format
	sortByFormatStage := bson.D{
		primitive.E{
			Key: "$sort", Value: bson.D{
				primitive.E{
					Key: "FormatId", Value: 1,
				},
			},
		},
	}
	// Sort teams in reverse chronological order
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
				usageProjectField,
			},
		},
	}

	// Initialize pipeline stages
	pipelineStages := []bson.D{sortByFormatStage, sortByDateStage, groupUsageResponseStage}
	// Add intermediate aggregation stages
	pipelineStages = append(pipelineStages, intermediateStages...)

	return pipelineStages
}

func MakeTimeSeriesUsageQueryPipeline(pokemon string, intermediateStages []bson.D) []bson.D {
	// Sort usage in reverse chronological order
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
