package utils

import (
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

// Generates a aggregation pipeline for team queries.
// Prepends team unwinding and reverse chronological sorting.
// Includes Pokémon query if parameter provided.
func MakeTeamQueryPipeline(pokemon string, intermediateStages []bson.D) []bson.D {
	// Unwind team replay information
	unwindTeamStage := bson.D{
		primitive.E{
			Key: "$unwind", Value: bson.D{
				primitive.E{
					Key: "path", Value: "$Teams",
				},
			},
		},
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
	// Sort teams by rating
	sortByRatingStage := bson.D{
		primitive.E{
			Key: "$sort", Value: bson.D{
				primitive.E{
					Key: "Rating", Value: -1,
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

	// Initialize pipeline stages
	pipelineStages := []bson.D{unwindTeamStage, sortByFormatStage, sortByRatingStage, sortByDateStage}
	// Add intermediate aggregation stages
	pipelineStages = append(pipelineStages, intermediateStages...)

	// Match all teams with Pokémon if provided
	if pokemon != "" {
		pipelineStages = append(pipelineStages, bson.D{
			primitive.E{
				Key: "$match", Value: bson.D{
					primitive.E{
						Key: "Teams.PokemonRoster", Value: pokemon,
					},
				},
			},
		})
	}

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

// Paginate aggregation results through slicing.
func SliceResults(results []bson.M, skip int, size int) []bson.M {
	// Limit skip to length of results
	if skip > len(results) {
		skip = len(results)
	}

	end := skip + size

	// Limit end to length of results
	if end > len(results) {
		end = len(results)
	}

	return results[skip:end]
}
