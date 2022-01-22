package utils

import (
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

// Generates a aggregation pipeline for team queries.
// Prepends team unwinding and reverse chronological sorting.
// Appends skip and limit queries if parameters provided.
func MakeTeamQueryPipeline(page int, limit int, pokemon string, intermediateStages []bson.D) mongo.Pipeline {
	// Unwind team replay information
	unwindTeamStage := bson.D{
		primitive.E{
			Key: "$unwind", Value: bson.D{
				primitive.E{
					Key: "path", Value: "$teams",
				},
			},
		},
	}
	// Sort teams in reverse chronological order
	sortByDateStage := bson.D{
		primitive.E{
			Key: "$sort", Value: bson.D{
				primitive.E{
					Key: "date", Value: -1,
				},
			},
		},
	}
	// Skip to page requested
	skipToPageStage := bson.D{
		primitive.E{
			Key: "$skip", Value: page,
		},
	}
	// Limit number of results
	limitStage := bson.D{
		primitive.E{
			Key: "$limit", Value: limit,
		},
	}

	// Initialize pipeline stages
	pipelineStages := []bson.D{unwindTeamStage, sortByDateStage}
	// Add intermediate aggregation stages
	pipelineStages = append(pipelineStages, intermediateStages...)

	// Match all teams with Pokémon if provided
	if pokemon != "" {
		pipelineStages = append(pipelineStages, bson.D{
			primitive.E{
				Key: "$match", Value: bson.D{
					primitive.E{
						Key: "teams.pokemon_roster", Value: pokemon,
					},
				},
			},
		})
	}

	// Finish pipeline with skip and limit if provided
	pipelineStages = append(pipelineStages, skipToPageStage)
	// Verify limit parameter is valid
	if limit != 0 {
		pipelineStages = append(pipelineStages, limitStage)
	}

	return pipelineStages
}
