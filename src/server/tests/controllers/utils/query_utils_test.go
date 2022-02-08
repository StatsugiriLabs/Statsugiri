package tests

import (
	"testing"

	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/stretchr/testify/assert"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

// Create mock team snapshots
func createMockTeamSnapshots() []models.PokemonTeamsSnapshot {
	return []models.PokemonTeamsSnapshot{
		{
			Date:     "2022-01-01",
			FormatId: "gen8vgc2021series11",
			Teams: []models.Team{
				{
					PokemonRoster:    []string{"a11", "b11", "c11"},
					Rating:           1511,
					ReplayUploadDate: "2022-01-01",
				},
				{
					PokemonRoster:    []string{"a12", "b12", "c12"},
					Rating:           1512,
					ReplayUploadDate: "2022-01-02",
				},
			},
		},
		{
			Date:     "2022-01-02",
			FormatId: "gen8vgc2021series11",
			Teams: []models.Team{
				{
					PokemonRoster:    []string{"a21", "b21", "c21"},
					Rating:           1521,
					ReplayUploadDate: "2022-02-01",
				},
				{
					PokemonRoster:    []string{"a22", "b22", "c22"},
					Rating:           1522,
					ReplayUploadDate: "2022-02-02",
				},
			},
		},
		{
			Date:     "2022-01-03",
			FormatId: "gen8vgc2021series11",
			Teams: []models.Team{
				{
					PokemonRoster:    []string{"a31", "b31", "c31"},
					Rating:           1531,
					ReplayUploadDate: "2022-03-01",
				},
				{
					PokemonRoster:    []string{"a32", "b32", "c32"},
					Rating:           1532,
					ReplayUploadDate: "2022-03-02",
				},
			},
		},
		{
			Date:     "2022-01-04",
			FormatId: "gen8vgc2021series11",
			Teams: []models.Team{
				{
					PokemonRoster:    []string{"a41", "b41", "c41"},
					Rating:           1541,
					ReplayUploadDate: "2022-04-01",
				},
				{
					PokemonRoster:    []string{"a42", "b42", "c42"},
					Rating:           1542,
					ReplayUploadDate: "2022-04-02",
				},
			},
		},
	}
}

// Test making query pipelines.
func TestMakeTeamQueryPipelineHappyPath(t *testing.T) {
	pokemon := "Pikachu"
	intermediateStages := bson.M{
		"$match": bson.M{
			"TestKey": "TestValue",
		},
	}

	expectedPipelinePokemonFilter := []bson.M{
		{"$unwind": "$Teams"},
		{"$sort": bson.M{"Rating": -1}},
		intermediateStages,
		{
			"$match": bson.M{
				"Teams.PokemonRoster": pokemon,
			},
		},
		{
			"$group": bson.M{
				"_id":      "$_id",
				"Date":     bson.M{"$first": "$Date"},
				"FormatId": bson.M{"$first": "$FormatId"},
				"Teams":    bson.M{"$push": "$Teams"},
			},
		},
		{"$sort": bson.D{
			primitive.E{Key: "Date", Value: -1},
			primitive.E{Key: "FormatId", Value: -1},
		}},
	}

	expectedPipeline := []bson.M{
		{"$unwind": "$Teams"},
		{"$sort": bson.M{"Rating": -1}},
		intermediateStages,
		{
			"$group": bson.M{
				"_id":      "$_id",
				"Date":     bson.M{"$first": "$Date"},
				"FormatId": bson.M{"$first": "$FormatId"},
				"Teams":    bson.M{"$push": "$Teams"},
			},
		},
		{"$sort": bson.D{
			primitive.E{Key: "Date", Value: -1},
			primitive.E{Key: "FormatId", Value: -1},
		}},
	}

	// Generate pipeline with Pokémon filter
	pipeline := utils.MakeTeamQueryPipeline(pokemon, []bson.M{intermediateStages})
	assert.Equal(t, pipeline, expectedPipelinePokemonFilter, "Pipelines do not match.")
	// Generate pipeline without Pokémon filter
	pipeline = utils.MakeTeamQueryPipeline("", []bson.M{intermediateStages})
	assert.Equal(t, pipeline, expectedPipeline, "Pipelines do not match.")
}

// Test making generic usage query pipelines.
func TestMakeUsageQueryPipelineUsage(t *testing.T) {
	intermediateStages := bson.M{
		"$match": bson.M{
			"TestKey": "TestValue",
		},
	}

	expectedPipeline := []bson.M{
		{"$sort": bson.D{
			primitive.E{Key: "Date", Value: -1},
			primitive.E{Key: "FormatId", Value: -1},
		}},
		{
			"$project": bson.M{
				"_id":                       false,
				"Date":                      1,
				"FormatId":                  1,
				"PokemonUsage":              1,
				"PokemonPartnerUsage":       1,
				"PokemonAverageRatingUsage": 1,
			},
		},
		intermediateStages,
	}

	pipeline := utils.MakeUsageQueryPipeline(utils.Usage, []bson.M{intermediateStages})
	assert.Equal(t, pipeline, expectedPipeline, "Pipelines do not match.")
}

// Test creating composite key.
func TestMakeCompositeKeyHappyPath(t *testing.T) {
	expectedCompositeKey := "test1test2"
	compositeKey := utils.MakeCompositeKey("test1", "test2")
	assert.Equal(t, compositeKey, expectedCompositeKey, "Composite keys do not match.")
}

// Test slicing team results for single page.
func TestSliceResultsHappyPath(t *testing.T) {
	results := createMockTeamSnapshots()
	expectedPaginatedResults := results[:2]
	paginatedResults := utils.SliceTeamSnapshots(results, 0, 2)
	assert.Equal(t, paginatedResults, expectedPaginatedResults, "Paginated results do not match.")
}

// Test when returning last paginated results with leftover results.
func TestSliceResultsLastPageNotFull(t *testing.T) {
	results := createMockTeamSnapshots()
	// Expect the last result
	expectedPaginatedResults := results[len(results)-1:]
	// Skip all but last snapshot with a size of 2, giving 1 snapshot remaining
	paginatedResults := utils.SliceTeamSnapshots(results, len(results)-1, 2)
	assert.Equal(t, paginatedResults, expectedPaginatedResults, "Paginated results do not match.")
}

// Test when page has no results (eg. beyond boundaries).
func TestSliceResultsInvalidPage(t *testing.T) {
	results := createMockTeamSnapshots()
	// Paginate beyond number of available results
	paginatedResults := utils.SliceTeamSnapshots(results, len(results)+1, 1)
	assert.Equal(t, paginatedResults, []models.PokemonTeamsSnapshot{}, "Paginated results do not match.")
}
