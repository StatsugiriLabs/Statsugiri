package tests

import (
	"testing"

	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/responses"
	"github.com/kelvinkoon/babiri_v2/transformers"
	"github.com/stretchr/testify/assert"
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

func getExpectedHappyPathResponse() responses.TeamsResponse {
	mockPokemonTeamSnapshots := []responses.PokemonTeamsSnapshot{
		{
			Date:     "2022-01-01",
			FormatId: "gen8vgc2021series11",
			Teams: []responses.Team{
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
			Teams: []responses.Team{
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
			Teams: []responses.Team{
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
			Teams: []responses.Team{
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
	return responses.TeamsResponse{
		NumResults:            4,
		Page:                  1,
		Limit:                 5,
		PokemonTeamsSnapshots: mockPokemonTeamSnapshots,
	}
}

func getExpectedNoSnapshotResponse() responses.TeamsResponse {
	return responses.TeamsResponse{
		NumResults:            0,
		Page:                  1,
		Limit:                 5,
		PokemonTeamsSnapshots: []responses.PokemonTeamsSnapshot{},
	}
}

// Test transforming team snapshots to response successfully.
func TestTransformTeamSnapshotsToResponseHappyPath(t *testing.T) {
	teamSnapshots := createMockTeamSnapshots()
	response := transformers.TransformTeamSnapshotsToResponse(teamSnapshots, 0, 5)
	assert.Equal(t, response, getExpectedHappyPathResponse())
}

// Test transforming team snapshots to response when no snapshots given.
func TestTransformTeamSnapshotsToResponseNoSnapshotsProvided(t *testing.T) {
	response := transformers.TransformTeamSnapshotsToResponse([]models.PokemonTeamsSnapshot{}, 0, 5)
	assert.Equal(t, response, getExpectedNoSnapshotResponse())
}
