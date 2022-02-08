package tests

import (
	"testing"

	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/responses"
	"github.com/kelvinkoon/babiri_v2/transformers"
	"github.com/stretchr/testify/assert"
)

func getExpectedFormatSet() map[string]bool {
	formatSet := make(map[string]bool)
	formatSet["gen8vgc2021series11"] = true
	formatSet["gen8ou"] = true
	return formatSet
}

func getExpectedTimeSeriesResponseHappyPath() responses.TimeSeriesUsageResponse {
	responseFormatUsageSnapshots := []responses.FormatUsageSnapshot{
		{
			FormatId: "gen8ou",
			TimeSeriesUsageSnapshots: []responses.TimeSeriesUsageSnapshot{
				{
					Date:  "2022-01-03",
					Usage: 0,
				},
				{
					Date:  "2022-01-04",
					Usage: 0,
				},
			},
		},
		{
			FormatId: "gen8vgc2021series11",
			TimeSeriesUsageSnapshots: []responses.TimeSeriesUsageSnapshot{
				{
					Date:  "2022-01-01",
					Usage: 0,
				},
				{
					Date:  "2022-01-02",
					Usage: 0,
				},
			},
		},
	}

	return responses.TimeSeriesUsageResponse{
		NumResults:           2,
		Pokemon:              "Pikachu",
		FormatUsageSnapshots: responseFormatUsageSnapshots,
	}
}

func getExpectedTimeSeriesResponseNoSnapshots() responses.TimeSeriesUsageResponse {
	return responses.TimeSeriesUsageResponse{
		NumResults:           0,
		Pokemon:              "Pikachu",
		FormatUsageSnapshots: []responses.FormatUsageSnapshot{},
	}
}

// Test format ID set extraction from usage snapshots successfully.
func TestGetFormatIdHappyPath(t *testing.T) {
	mockSnapshots := CreateMockUsageSnapshots()
	formatSet := transformers.GetFormatIdSet(mockSnapshots)
	assert.Equal(t, formatSet, getExpectedFormatSet())
}

// Test transforming usage models to time series usage response successfully.
func TestTransformUsageSnapshotsToTimeSeriesResponseHappyPath(t *testing.T) {
	mockSnapshots := CreateMockUsageSnapshots()
	response := transformers.TransformUsageSnapshotsToTimeSeriesResponse("Pikachu", mockSnapshots)
	assert.Equal(t, response, getExpectedTimeSeriesResponseHappyPath())
}

// Test transforming usage models to time series usage response successfully.
func TestTransformUsageSnapshotsToTimeSeriesResponseNoSnapshots(t *testing.T) {
	response := transformers.TransformUsageSnapshotsToTimeSeriesResponse("Pikachu", []models.PokemonUsageSnapshot{})
	assert.Equal(t, response, getExpectedTimeSeriesResponseNoSnapshots())
}
