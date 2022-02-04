package transformers

import (
	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/responses"
)

// Convert PokemonUsageSnapshots models to a TimeSeriesUsageResponse.
func TransformUsageSnapshotsToResponse(pokemon string, snapshots []models.PokemonUsageSnapshot) responses.TimeSeriesUsageResponse {
	// Retrieve set of formats
	formatIdSet := GetFormatIdSet(snapshots)

	// Create formatUsageSnapshots from formatIdSet
	var formatUsageSnapshots []responses.FormatUsageSnapshot
	for formatId := range formatIdSet {
		// Create record of time series usage snapshots
		var timeSeriesUsageSnapshots []responses.TimeSeriesUsageSnapshot
		for _, snapshot := range snapshots {
			if snapshot.FormatId == formatId {
				var timeSeriesUsageSnapshot responses.TimeSeriesUsageSnapshot
				timeSeriesUsageSnapshot.Date = snapshot.Date
				usage, found := snapshot.PokemonUsage[pokemon]
				if found {
					timeSeriesUsageSnapshot.Usage = usage
				} else {
					timeSeriesUsageSnapshot.Usage = 0
				}
				timeSeriesUsageSnapshots = append(timeSeriesUsageSnapshots, timeSeriesUsageSnapshot)
			}
		}

		// Create FormatUsageSnapshot
		var formatUsageSnapshot responses.FormatUsageSnapshot
		formatUsageSnapshot.FormatId = formatId
		formatUsageSnapshot.TimeSeriesUsageSnapshots = timeSeriesUsageSnapshots
		formatUsageSnapshots = append(formatUsageSnapshots, formatUsageSnapshot)
	}

	// Create response
	var response responses.TimeSeriesUsageResponse
	response.Pokemon = pokemon
	response.FormatUsageSnapshots = formatUsageSnapshots
	return response
}

// Create a unique set of format IDs from snapshots.
func GetFormatIdSet(snapshots []models.PokemonUsageSnapshot) map[string]bool {
	// Filter for unique formats in results
	formatIdList := make(map[string]bool)
	for _, snapshot := range snapshots {
		if _, found := formatIdList[snapshot.FormatId]; !found {
			formatIdList[snapshot.FormatId] = true
		}
	}
	return formatIdList
}
