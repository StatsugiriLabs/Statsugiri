package transformers

import (
	"sort"

	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/responses"
)

// Convert PokemonUsageSnapshots models to a TimeSeriesUsageResponse.
func TransformUsageSnapshotsToTimeSeriesResponse(pokemon string, snapshots []models.PokemonUsageSnapshot) responses.TimeSeriesUsageResponse {
	// Retrieve set of formats
	formatIdSet := GetFormatIdSet(snapshots)

	// Create formatUsageSnapshots from formatIdSet
	var formatUsageSnapshots []responses.FormatUsageSnapshot
	for formatId := range formatIdSet {
		// Create record of time series usage snapshots
		var timeSeriesUsageSnapshots []responses.TimeSeriesUsageSnapshot
		for _, snapshot := range snapshots {
			// Create record for snapshot matching the format ID
			if snapshot.FormatId == formatId {
				usage, found := snapshot.PokemonUsage[pokemon]
				// Substitute empty usage with 0
				if !found {
					usage = 0
				}

				timeSeriesUsageSnapshot := responses.TimeSeriesUsageSnapshot{
					Date:  snapshot.Date,
					Usage: usage,
				}
				timeSeriesUsageSnapshots = append(timeSeriesUsageSnapshots, timeSeriesUsageSnapshot)
			}
		}

		// Create FormatUsageSnapshot
		formatUsageSnapshot := responses.FormatUsageSnapshot{
			FormatId:                 formatId,
			TimeSeriesUsageSnapshots: timeSeriesUsageSnapshots,
		}
		formatUsageSnapshots = append(formatUsageSnapshots, formatUsageSnapshot)
	}

	// Sort snapshots by format alphabetically
	sort.Slice(formatUsageSnapshots, func(i, j int) bool {
		return formatUsageSnapshots[i].FormatId <
			formatUsageSnapshots[j].FormatId
	})

	// Replace no results with empty snapshot list
	var responseFormatUsageSnapshots []responses.FormatUsageSnapshot
	if formatUsageSnapshots == nil {
		responseFormatUsageSnapshots = []responses.FormatUsageSnapshot{}
	} else {
		responseFormatUsageSnapshots = formatUsageSnapshots
	}

	return responses.TimeSeriesUsageResponse{
		NumResults:           len(formatUsageSnapshots),
		Pokemon:              pokemon,
		FormatUsageSnapshots: responseFormatUsageSnapshots,
	}
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
