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
		var pokemonUsages []responses.PokemonUsage
		for pokemon, usage := range snapshot.PokemonUsage {
			pokemonUsage := responses.PokemonUsage{
				Pokemon: pokemon,
				Usage:   usage,
			}
			pokemonUsages = append(pokemonUsages, pokemonUsage)
		}

		usageSnapshot := responses.UsageSnapshot{
			Date:          snapshot.Date,
			FormatId:      snapshot.FormatId,
			PokemonUsages: pokemonUsages,
		}
		usageSnapshots = append(usageSnapshots, usageSnapshot)
	}

	// Replace no results with empty snapshot list
	var responseUsageSnapshots []responses.UsageSnapshot
	if usageSnapshots == nil {
		responseUsageSnapshots = []responses.UsageSnapshot{}
	} else {
		responseUsageSnapshots = usageSnapshots
	}

	return responses.UsageResponse{
		NumResults:     len(usageSnapshots),
		Page:           utils.SkipToPage(skip, limit),
		Limit:          limit,
		UsageSnapshots: responseUsageSnapshots,
	}
}

// Convert PokemonUsageSnapshot models to a RatingUsageResponse.
func TransformRatingUsageSnapshotsToRatingUsageResponse(snapshots []models.PokemonUsageSnapshot, skip int, limit int) responses.RatingUsageResponse {
	// Create record of rating usage snapshots
	var ratingUsageSnapshots []responses.RatingUsageSnapshot

	// Iterate through internal usage snapshots
	for _, snapshot := range snapshots {
		var pokemonAverageRatingUsages []responses.PokemonAverageRatingUsage
		for pokemon, avgRatingUsage := range snapshot.PokemonAverageRatingUsage {
			pokemonAverageRatingUsage := responses.PokemonAverageRatingUsage{
				Pokemon:            pokemon,
				AverageRatingUsage: avgRatingUsage,
			}
			pokemonAverageRatingUsages = append(pokemonAverageRatingUsages, pokemonAverageRatingUsage)
		}
		ratingUsageSnapshot := responses.RatingUsageSnapshot{
			Date:                       snapshot.Date,
			FormatId:                   snapshot.FormatId,
			PokemonAverageRatingUsages: pokemonAverageRatingUsages,
		}
		ratingUsageSnapshots = append(ratingUsageSnapshots, ratingUsageSnapshot)
	}

	// Replace no results with empty snapshot list
	var responseRatingUsageSnapshots []responses.RatingUsageSnapshot
	if ratingUsageSnapshots == nil {
		responseRatingUsageSnapshots = []responses.RatingUsageSnapshot{}
	} else {
		responseRatingUsageSnapshots = ratingUsageSnapshots
	}

	return responses.RatingUsageResponse{
		NumResults:           len(ratingUsageSnapshots),
		Page:                 utils.SkipToPage(skip, limit),
		Limit:                limit,
		RatingUsageSnapshots: responseRatingUsageSnapshots,
	}
}

// Convert PartnerUsageSnapshot models to a PartnerUsageResponse.
func TransformPartnerUsageSnapshotsToPartnerUsageResponse(snapshots []models.PokemonUsageSnapshot, skip int, limit int) responses.PartnerUsageResponse {
	// Create record of partner usage snapshots
	var partnerUsageSnapshots []responses.PartnerUsageSnapshot

	// Iterate through internal usage snapshots
	for _, snapshot := range snapshots {
		var pokemonPartnerUsages []responses.PokemonPartnerUsage
		for pokemon, snapshotPartnerUsages := range snapshot.PokemonPartnerUsage {
			var partnerUsages []responses.PartnerUsage
			for partner, usage := range snapshotPartnerUsages {
				partnerUsage := responses.PartnerUsage{
					Partner: partner,
					Usage:   usage,
				}
				partnerUsages = append(partnerUsages, partnerUsage)
			}
			pokemonPartnerUsage := responses.PokemonPartnerUsage{
				Pokemon:       pokemon,
				PartnerUsages: partnerUsages,
			}
			pokemonPartnerUsages = append(pokemonPartnerUsages, pokemonPartnerUsage)
		}
		partnerUsageSnapshot := responses.PartnerUsageSnapshot{
			Date:                 snapshot.Date,
			FormatId:             snapshot.FormatId,
			PokemonPartnerUsages: pokemonPartnerUsages,
		}
		partnerUsageSnapshots = append(partnerUsageSnapshots, partnerUsageSnapshot)
	}

	// Replace no results with empty snapshot list
	var responsePartnerUsageSnapshots []responses.PartnerUsageSnapshot
	if partnerUsageSnapshots == nil {
		responsePartnerUsageSnapshots = []responses.PartnerUsageSnapshot{}
	} else {
		responsePartnerUsageSnapshots = partnerUsageSnapshots
	}

	return responses.PartnerUsageResponse{
		NumResults:            len(partnerUsageSnapshots),
		Page:                  utils.SkipToPage(skip, limit),
		Limit:                 limit,
		PartnerUsageSnapshots: responsePartnerUsageSnapshots,
	}
}
