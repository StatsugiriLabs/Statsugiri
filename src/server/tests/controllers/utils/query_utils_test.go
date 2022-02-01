package tests

import (
	"testing"

	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	"github.com/stretchr/testify/assert"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

// Create mock team snapshots
func createMockTeamSnapshots() []bson.M {
	return []bson.M{
		{
			"Date":     "2022-01-26",
			"FormatId": "gen8vgc2021series11",
			"Teams": bson.M{
				"PokemonRoster": bson.A{
					[]string{
						"Calyrex-Shadow",
						"Whimsicott",
						"Urshifu",
						"Tapu Lele",
						"Thundurus",
						"Chandelure",
					},
				},
			},
			"Rating":           1710,
			"ReplayUploadDate": "2022-01-09",
		},
		{
			"Date":     "2022-01-26",
			"FormatId": "gen8vgc2021series11",
			"Teams": bson.M{
				"PokemonRoster": bson.A{
					[]string{
						"Naganadel",
						"Tornadus",
						"Dracovish",
						"Mienshao",
						"Chandelure",
						"Tsareena",
					},
				},
				"Rating":           1690,
				"ReplayUploadDate": "2022-01-16",
			},
		},
		{
			"Date":     "2022-01-26",
			"FormatId": "gen8vgc2021series11",
			"Teams": bson.M{
				"PokemonRoster": bson.A{
					[]string{
						"Rillaboom",
						"Urshifu",
						"Coalossal",
						"Thundurus",
						"Zacian",
						"Incineroar",
					},
				},
				"Rating":           1679,
				"ReplayUploadDate": "2021-12-01",
			},
		},
		{
			"Date":     "2022-01-26",
			"FormatId": "gen8vgc2021series11",
			"Teams": bson.M{
				"PokemonRoster": bson.A{
					[]string{
						"Kyogre",
						"Calyrex-Ice",
						"Incineroar",
						"Mimikyu",
						"Venusaur",
						"Regieleki",
					},
				},
				"Rating":           1651,
				"ReplayUploadDate": "2022-01-01",
			},
		},
		{
			"Date":     "2022-01-26",
			"FormatId": "gen8vgc2021series11",
			"Teams": bson.M{
				"PokemonRoster": bson.A{
					[]string{
						"Zacian",
						"Lapras",
						"Thundurus",
						"Landorus-Therian",
						"Urshifu",
						"Incineroar",
					},
				},
				"Rating":           1646,
				"ReplayUploadDate": "2021-12-28",
			},
		},
	}
}

// Test making query pipelines.
func TestMakeTeamQueryPipelineHappyPath(t *testing.T) {
	pokemon := "Pikachu"
	intermediateStages := bson.D{
		primitive.E{Key: "$match", Value: bson.D{
			primitive.E{
				Key: "TestKey", Value: "TestValue",
			},
		}},
	}

	expectedPipeline := []bson.D{
		{
			primitive.E{
				Key: "$unwind", Value: bson.D{
					primitive.E{
						Key: "path", Value: "$Teams",
					},
				},
			},
		},
		{
			primitive.E{
				Key: "$sort", Value: bson.D{
					primitive.E{
						Key: "FormatId", Value: 1,
					},
				},
			},
		},
		{
			primitive.E{
				Key: "$sort", Value: bson.D{
					primitive.E{
						Key: "Rating", Value: -1,
					},
				},
			},
		},
		{
			primitive.E{
				Key: "$sort", Value: bson.D{
					primitive.E{
						Key: "Date", Value: -1,
					},
				},
			},
		},
		{
			primitive.E{
				Key: "$project", Value: bson.D{
					primitive.E{
						Key: "Date", Value: 1,
					},
					primitive.E{
						Key: "FormatId", Value: 1,
					},
					primitive.E{
						Key: "Teams", Value: 1,
					},
					primitive.E{
						Key: "Rating", Value: 1,
					},
					primitive.E{
						Key: "ReplayUploadDate", Value: 1,
					},
					primitive.E{
						Key: "_id", Value: 0,
					},
				},
			},
		},
		intermediateStages,
		{
			primitive.E{
				Key: "$match", Value: bson.D{
					primitive.E{
						Key: "Teams.PokemonRoster", Value: pokemon,
					},
				},
			},
		},
	}

	// Generate pipeline with Pokémon filter
	pipeline := utils.MakeTeamQueryPipeline(pokemon, []bson.D{intermediateStages})
	assert.Equal(t, pipeline, expectedPipeline, "Pipelines do not match.")
	// Generate pipeline without Pokémon filter
	pipeline = utils.MakeTeamQueryPipeline("", []bson.D{intermediateStages})
	assert.Equal(t, pipeline, expectedPipeline[:len(expectedPipeline)-1], "Pipelines do not match.")
}

// Test making query pipelines for usage.
func TestMakeUsageQueryPipelineUsage(t *testing.T) {
	intermediateStages := bson.D{
		primitive.E{Key: "$match", Value: bson.D{
			primitive.E{
				Key: "TestKey", Value: "TestValue",
			},
		}},
	}

	expectedPipeline := []bson.D{
		{
			primitive.E{
				Key: "$sort", Value: bson.D{
					primitive.E{
						Key: "FormatId", Value: 1,
					},
				},
			},
		},
		{
			primitive.E{
				Key: "$sort", Value: bson.D{
					primitive.E{
						Key: "Date", Value: -1,
					},
				},
			},
		},
		{
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
						Key: "PokemonUsage", Value: 1,
					},
				},
			},
		},
		intermediateStages,
	}

	pipeline := utils.MakeUsageQueryPipeline(utils.Usage, []bson.D{intermediateStages})
	assert.Equal(t, pipeline, expectedPipeline, "Pipelines do not match.")
}

// Test making query pipelines for partner usage.
func TestMakeUsageQueryPipelinePartnerUsage(t *testing.T) {
	intermediateStages := bson.D{
		primitive.E{Key: "$match", Value: bson.D{
			primitive.E{
				Key: "TestKey", Value: "TestValue",
			},
		}},
	}

	expectedPipeline := []bson.D{
		{
			primitive.E{
				Key: "$sort", Value: bson.D{
					primitive.E{
						Key: "FormatId", Value: 1,
					},
				},
			},
		},
		{
			primitive.E{
				Key: "$sort", Value: bson.D{
					primitive.E{
						Key: "Date", Value: -1,
					},
				},
			},
		},
		{
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
						Key: "PokemonPartnerUsage", Value: 1,
					},
				},
			},
		},
		intermediateStages,
	}

	pipeline := utils.MakeUsageQueryPipeline(utils.PartnerUsage, []bson.D{intermediateStages})
	assert.Equal(t, pipeline, expectedPipeline, "Pipelines do not match.")
}

// Test making query pipelines for average rating usage.
func TestMakeUsageQueryPipelineAverageRatingUsage(t *testing.T) {
	intermediateStages := bson.D{
		primitive.E{Key: "$match", Value: bson.D{
			primitive.E{
				Key: "TestKey", Value: "TestValue",
			},
		}},
	}

	expectedPipeline := []bson.D{
		{
			primitive.E{
				Key: "$sort", Value: bson.D{
					primitive.E{
						Key: "FormatId", Value: 1,
					},
				},
			},
		},
		{
			primitive.E{
				Key: "$sort", Value: bson.D{
					primitive.E{
						Key: "Date", Value: -1,
					},
				},
			},
		},
		{
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
						Key: "PokemonAverageRatingUsage", Value: 1,
					},
				},
			},
		},
		intermediateStages,
	}

	pipeline := utils.MakeUsageQueryPipeline(utils.RatingUsage, []bson.D{intermediateStages})
	assert.Equal(t, pipeline, expectedPipeline, "Pipelines do not match.")
}

// Test creating composite key.
func TestMakeCompositeKeyHappyPath(t *testing.T) {
	expectedCompositeKey := "test1test2"
	compositeKey := utils.MakeCompositeKey("test1", "test2")
	assert.Equal(t, compositeKey, expectedCompositeKey, "Composite keys do not match.")
}

// Test slicing results for single page.
func TestSliceResultsHappyPath(t *testing.T) {
	results := createMockTeamSnapshots()
	expectedPaginatedResults := results[:2]
	paginatedResults := utils.SliceResults(results, 0, 2)
	assert.Equal(t, paginatedResults, expectedPaginatedResults, "Paginated results do not match.")
}

// Test when returning last paginated results with leftover results.
func TestSliceResultsLastPageNotFull(t *testing.T) {
	results := createMockTeamSnapshots()
	// Expect the last result
	expectedPaginatedResults := results[len(results)-1:]
	// Skip all but last snapshot with a size of 2, giving 1 snapshot remaining
	paginatedResults := utils.SliceResults(results, len(results)-1, 2)
	assert.Equal(t, paginatedResults, expectedPaginatedResults, "Paginated results do not match.")
}

// Test when page has no results (eg. beyond boundaries).
func TestSliceResultsInvalidPage(t *testing.T) {
	results := createMockTeamSnapshots()
	// Paginate beyond number of available results
	paginatedResults := utils.SliceResults(results, len(results)+1, 1)
	assert.Equal(t, paginatedResults, []bson.M{}, "Paginated results do not match.")
}
