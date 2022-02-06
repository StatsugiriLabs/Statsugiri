package transformers

import (
	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/responses"
)

// Convert PokemonUsageSnapshot models to a UsageResponse.
func TransformUsageSnapshotsToUsageResponse(snapshots []models.PokemonUsageSnapshot, skip int, limit int) responses.UsageResponse {
	// Create record of time series usage snapshots
	var usageSnapshots []responses.UsageSnapshot
	for _, snapshot := range snapshots {
		var usageSnapshot responses.UsageSnapshot
		usageSnapshot.Date = snapshot.Date
		usageSnapshot.FormatId = snapshot.FormatId
		var pokemonUsages []responses.PokemonUsage
		for pokemon, usage := range snapshot.PokemonUsage {
			var pokemonUsage responses.PokemonUsage
			pokemonUsage.Pokemon = pokemon
			pokemonUsage.Usage = usage
			pokemonUsages = append(pokemonUsages, pokemonUsage)
		}
		usageSnapshot.PokemonUsages = pokemonUsages
		usageSnapshots = append(usageSnapshots, usageSnapshot)
	}

	var response responses.UsageResponse
	response.NumResults = len(usageSnapshots)
	response.Page = utils.SkipToPage(skip, limit)
	response.Limit = limit
	if usageSnapshots == nil {
		response.UsageSnapshots = []responses.UsageSnapshot{}
	} else {
		response.UsageSnapshots = usageSnapshots
	}
	return response
}

// Convert PokemonUsageSnapshot models to a RatingUsageResponse.
func TransformRatingUsageSnapshotsToRatingUsageResponse(snapshots []models.PokemonUsageSnapshot, skip int, limit int) responses.RatingUsageResponse {
	// Create record of time series usage snapshots
	var ratingUsageSnapshots []responses.RatingUsageSnapshot
	for _, snapshot := range snapshots {
		var ratingUsageSnapshot responses.RatingUsageSnapshot
		ratingUsageSnapshot.Date = snapshot.Date
		ratingUsageSnapshot.FormatId = snapshot.FormatId
		var pokemonAverageRatingUsages []responses.PokemonAverageRatingUsage
		for pokemon, ratingUsage := range snapshot.PokemonUsage {
			var pokemonAverageRatingUsage responses.PokemonAverageRatingUsage
			pokemonAverageRatingUsage.Pokemon = pokemon
			pokemonAverageRatingUsage.AverageRatingUsage = ratingUsage
			pokemonAverageRatingUsages = append(pokemonAverageRatingUsages, pokemonAverageRatingUsage)
		}
		ratingUsageSnapshot.PokemonAverageRatingUsages = pokemonAverageRatingUsages
		ratingUsageSnapshots = append(ratingUsageSnapshots, ratingUsageSnapshot)
	}

	var response responses.RatingUsageResponse
	response.NumResults = len(ratingUsageSnapshots)
	response.Page = utils.SkipToPage(skip, limit)
	response.Limit = limit
	if ratingUsageSnapshots == nil {
		response.RatingUsageSnapshots = []responses.RatingUsageSnapshot{}
	} else {
		response.RatingUsageSnapshots = ratingUsageSnapshots
	}
	return response
}
