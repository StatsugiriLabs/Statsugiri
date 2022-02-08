package tests

import (
	"testing"

	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/responses"
	"github.com/kelvinkoon/babiri_v2/transformers"
	"github.com/stretchr/testify/assert"
)

func getExpectedUsageHappyPathResponse() responses.UsageResponse {
	mockPokemonUsageSnapshots := []responses.UsageSnapshot{
		{
			Date:          "2022-01-01",
			FormatId:      "gen8vgc2021series11",
			PokemonUsages: []responses.PokemonUsage(nil),
		},
		{
			Date:          "2022-01-02",
			FormatId:      "gen8vgc2021series11",
			PokemonUsages: []responses.PokemonUsage(nil),
		},
		{
			Date:          "2022-01-03",
			FormatId:      "gen8ou",
			PokemonUsages: []responses.PokemonUsage(nil),
		},
		{
			Date:          "2022-01-04",
			FormatId:      "gen8ou",
			PokemonUsages: []responses.PokemonUsage(nil),
		},
	}

	return responses.UsageResponse{
		NumResults:     4,
		Page:           1,
		Limit:          5,
		UsageSnapshots: mockPokemonUsageSnapshots,
	}
}

func getExpectedRatingUsageHappyPathResponse() responses.RatingUsageResponse {
	mockRatingUsageSnapshots := []responses.RatingUsageSnapshot{
		{
			Date:                       "2022-01-01",
			FormatId:                   "gen8vgc2021series11",
			PokemonAverageRatingUsages: []responses.PokemonAverageRatingUsage(nil),
		},
		{
			Date:                       "2022-01-02",
			FormatId:                   "gen8vgc2021series11",
			PokemonAverageRatingUsages: []responses.PokemonAverageRatingUsage(nil),
		},
		{
			Date:                       "2022-01-03",
			FormatId:                   "gen8ou",
			PokemonAverageRatingUsages: []responses.PokemonAverageRatingUsage(nil),
		},
		{
			Date:                       "2022-01-04",
			FormatId:                   "gen8ou",
			PokemonAverageRatingUsages: []responses.PokemonAverageRatingUsage(nil),
		},
	}

	return responses.RatingUsageResponse{
		NumResults:           4,
		Page:                 1,
		Limit:                5,
		RatingUsageSnapshots: mockRatingUsageSnapshots,
	}
}

func getExpectedPartnerUsageHappyPathResponse() responses.PartnerUsageResponse {
	mockPartnerUsageSnapshots := []responses.PartnerUsageSnapshot{
		{
			Date:                 "2022-01-01",
			FormatId:             "gen8vgc2021series11",
			PokemonPartnerUsages: []responses.PokemonPartnerUsage(nil),
		},
		{
			Date:                 "2022-01-02",
			FormatId:             "gen8vgc2021series11",
			PokemonPartnerUsages: []responses.PokemonPartnerUsage(nil),
		},
		{
			Date:                 "2022-01-03",
			FormatId:             "gen8ou",
			PokemonPartnerUsages: []responses.PokemonPartnerUsage(nil),
		},
		{
			Date:                 "2022-01-04",
			FormatId:             "gen8ou",
			PokemonPartnerUsages: []responses.PokemonPartnerUsage(nil),
		},
	}

	return responses.PartnerUsageResponse{
		NumResults:            4,
		Page:                  1,
		Limit:                 5,
		PartnerUsageSnapshots: mockPartnerUsageSnapshots,
	}
}

func getExpectedUsageNoSnapshotResponse() responses.UsageResponse {
	return responses.UsageResponse{
		NumResults:     0,
		Page:           1,
		Limit:          5,
		UsageSnapshots: []responses.UsageSnapshot{},
	}
}

func getExpectedRatingUsageNoSnapshotResponse() responses.RatingUsageResponse {
	return responses.RatingUsageResponse{
		NumResults:           0,
		Page:                 1,
		Limit:                5,
		RatingUsageSnapshots: []responses.RatingUsageSnapshot{},
	}
}

func getExpectedPartnerUsageNoSnapshotResponse() responses.PartnerUsageResponse {
	return responses.PartnerUsageResponse{
		NumResults:            0,
		Page:                  1,
		Limit:                 5,
		PartnerUsageSnapshots: []responses.PartnerUsageSnapshot{},
	}
}

// Test transforming usage snapshots to usage response successfully.
func TestTransformUsageTeamSnapshotsToUsageResponseHappyPath(t *testing.T) {
	usageSnapshots := CreateMockUsageSnapshots()
	response := transformers.TransformUsageSnapshotsToUsageResponse(usageSnapshots, 0, 5)
	assert.Equal(t, response, getExpectedUsageHappyPathResponse())
}

// Test transforming usage snapshots to response when no snapshots given.
func TestTransformUsageSnapshotsToUsageResponseNoSnapshotsProvided(t *testing.T) {
	response := transformers.TransformUsageSnapshotsToUsageResponse([]models.PokemonUsageSnapshot{}, 0, 5)
	assert.Equal(t, response, getExpectedUsageNoSnapshotResponse())
}

// Test transforming rating usage snapshots to rating usage response successfully.
func TestTransformRatingUsageTeamSnapshotsToRatingUsageResponseHappyPath(t *testing.T) {
	usageSnapshots := CreateMockUsageSnapshots()
	response := transformers.TransformRatingUsageSnapshotsToRatingUsageResponse(usageSnapshots, 0, 5)
	assert.Equal(t, response, getExpectedRatingUsageHappyPathResponse())
}

// Test transforming rating usage snapshots to response when no snapshots given.
func TestTransformRatingUsageSnapshotsToRatingUsageResponseNoSnapshotsProvided(t *testing.T) {
	response := transformers.TransformRatingUsageSnapshotsToRatingUsageResponse([]models.PokemonUsageSnapshot{}, 0, 5)
	assert.Equal(t, response, getExpectedRatingUsageNoSnapshotResponse())
}

// Test transforming partner usage snapshots to rating partner response successfully.
func TestTransformPartnerUsageTeamSnapshotsToPartnerUsageResponseHappyPath(t *testing.T) {
	usageSnapshots := CreateMockUsageSnapshots()
	response := transformers.TransformPartnerUsageSnapshotsToPartnerUsageResponse(usageSnapshots, 0, 5)
	assert.Equal(t, response, getExpectedPartnerUsageHappyPathResponse())
}

// Test transforming rating usage snapshots to response when no snapshots given.
func TestTransformPartnerUsageSnapshotsToPartnerUsageResponseNoSnapshotsProvided(t *testing.T) {
	response := transformers.TransformPartnerUsageSnapshotsToPartnerUsageResponse([]models.PokemonUsageSnapshot{}, 0, 5)
	assert.Equal(t, response, getExpectedPartnerUsageNoSnapshotResponse())
}
