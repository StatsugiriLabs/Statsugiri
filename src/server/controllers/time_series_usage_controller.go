package controllers

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	db "github.com/kelvinkoon/babiri_v2/db"
	"github.com/kelvinkoon/babiri_v2/errors"
	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/responses"
	log "github.com/sirupsen/logrus"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

func GetTimeSeriesUsageByPokemon() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// TODO: Parse query params for window of time
		pokemon := mux.Vars(r)["pokemon"]

		// Generate pipeline stages
		intermediateStages := []bson.D{}

		pipeline := utils.MakeTimeSeriesUsageQueryPipeline(pokemon, intermediateStages)
		queryTimeSeriesData(rw, pipeline, pokemon)
	}
}

func GetTimeSeriesUsageByPokemonFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// TODO: Parse query params for window of time
		pokemon := mux.Vars(r)["pokemon"]
		format := mux.Vars(r)["format"]
		if !utils.ValidFormat(format) {
			errors.CreateBadRequestErrorResponse(rw,
				fmt.Errorf("Format (%s) is not supported", format))
			return
		}

		// Generate pipeline stages
		intermediateStages := []bson.D{
			// Match usage by format
			{
				primitive.E{
					Key: "$match", Value: bson.D{
						primitive.E{
							Key: "FormatId", Value: format,
						},
					},
				},
			},
		}

		pipeline := utils.MakeTimeSeriesUsageQueryPipeline(pokemon, intermediateStages)
		queryTimeSeriesData(rw, pipeline, pokemon)
	}
}

// Queries usage collection using aggregation pipeline and encode results.
func queryTimeSeriesData(rw http.ResponseWriter, pipeline mongo.Pipeline, pokemon string) {
	start := time.Now()

	var snapshots []models.PokemonUsageSnapshot

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Run query with pipeline
	cursor, err := db.UsageCollection.Aggregate(ctx, pipeline)
	if err != nil {
		errors.CreateInternalServerErrorResponse(rw, err)
		return
	}
	defer cursor.Close(ctx)

	// Iterate and unmarshal through query results 
	if err = cursor.All(ctx, &snapshots); err != nil {
		panic(err)
	}

	// Filter for unique formats in results
	formatIdList := make(map[string]bool)
	for _, snapshot := range snapshots {
		if _, found := formatIdList[snapshot.FormatId]; !found {
			formatIdList[snapshot.FormatId] = true
		}
	}
	
	// Create formatUsageSnapshots from formatIdList
	var formatUsageSnapshots []responses.FormatUsageSnapshot
	for formatId := range formatIdList {
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

	log.Infof("Results returned in %s", time.Since(start))
	rw.WriteHeader(http.StatusOK)
	json.NewEncoder(rw).Encode(response)
}
