package transformers

import (
	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/responses"
)

// Convert PokemonTeamSnapshots models to a TeamsResponse.
func TransformTeamSnapshotsToResponse(snapshots []models.PokemonTeamsSnapshot, skip int, limit int) responses.TeamsResponse {
	// Create record of time series usage snapshots
	var pokemonTeamSnapshots []responses.PokemonTeamsSnapshot
	for _, snapshot := range snapshots {
		var pokemonTeamSnapshot responses.PokemonTeamsSnapshot
		pokemonTeamSnapshot.Date = snapshot.Date
		pokemonTeamSnapshot.FormatId = snapshot.FormatId
		// Convert internal model to response model
		var responseTeams []responses.Team
		for _, internalTeam := range snapshot.Teams {
			var responseTeam responses.Team
			responseTeam.PokemonRoster = internalTeam.PokemonRoster
			responseTeam.Rating = internalTeam.Rating
			responseTeam.ReplayUploadDate = internalTeam.ReplayUploadDate
			responseTeams = append(responseTeams, responseTeam)
		}
		pokemonTeamSnapshot.Teams = responseTeams
		pokemonTeamSnapshots = append(pokemonTeamSnapshots, pokemonTeamSnapshot)
	}

	// Create response
	var response responses.TeamsResponse
	response.NumResults = len(pokemonTeamSnapshots)
	response.Page = utils.SkipToPage(skip, limit)
	response.Limit = limit
	response.PokemonTeamsSnapshots = pokemonTeamSnapshots
	return response
}
