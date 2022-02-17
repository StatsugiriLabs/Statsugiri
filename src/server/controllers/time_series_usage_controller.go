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
	"github.com/kelvinkoon/babiri_v2/middleware"
	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/transformers"
	log "github.com/sirupsen/logrus"
	"go.mongodb.org/mongo-driver/bson"
)

func GetTimeSeriesUsageByPokemon() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		start, end, err := middleware.ParseStartAndEnd(rw, r)
		if err != nil {
			errors.CreateBadRequestErrorResponse(rw, err)
			return
		}

		pokemon := mux.Vars(r)["pokemon"]

		// Generate pipeline stages
		intermediateStages := []bson.M{}

		// Add start and end stages if provided
		if start != "" {
			intermediateStages = append(intermediateStages,
				bson.M{
					"$match": bson.M{
						"Date": bson.M{"$gte": start},
					},
				},
			)
		}

		if end != "" {
			intermediateStages = append(intermediateStages,
				bson.M{
					"$match": bson.M{
						"Date": bson.M{"$lte": end},
					},
				},
			)
		}

		pipeline := utils.MakeTimeSeriesUsageQueryPipeline(pokemon, intermediateStages)
		queryTimeSeriesData(rw, pipeline, pokemon)
	}
}

func GetTimeSeriesUsageByPokemonFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		start, end, err := middleware.ParseStartAndEnd(rw, r)
		if err != nil {
			errors.CreateBadRequestErrorResponse(rw, err)
			return
		}

		pokemon := mux.Vars(r)["pokemon"]
		format := mux.Vars(r)["format"]
		if !utils.ValidFormat(format) {
			errors.CreateBadRequestErrorResponse(rw,
				fmt.Errorf("Format (%s) is not supported", format))
			return
		}

		// Generate pipeline stages
		intermediateStages := []bson.M{
			// Match with format provided
			{
				"$match": bson.M{
					"FormatId": format,
				},
			},
		}

		// Add start and end stages if provided
		if start != "" {
			intermediateStages = append(intermediateStages,
				bson.M{
					"$match": bson.M{
						"Date": bson.M{"$gte": start},
					},
				},
			)
		}

		if end != "" {
			intermediateStages = append(intermediateStages,
				bson.M{
					"$match": bson.M{
						"Date": bson.M{"$lte": end},
					},
				},
			)
		}

		pipeline := utils.MakeTimeSeriesUsageQueryPipeline(pokemon, intermediateStages)
		queryTimeSeriesData(rw, pipeline, pokemon)
	}
}

// Queries usage collection using aggregation pipeline and encode results.
func queryTimeSeriesData(rw http.ResponseWriter, pipeline []bson.M, pokemon string) {
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

	// Write results to response
	writeTimeSeriesResponse(rw, snapshots, pokemon)
	log.Infof("Results returned in %s", time.Since(start))
}

// Transform internal models to response models and write to time series response.
func writeTimeSeriesResponse(rw http.ResponseWriter, snapshots []models.PokemonUsageSnapshot, pokemon string) {
	response := transformers.TransformUsageSnapshotsToTimeSeriesResponse(pokemon, snapshots)
	rw.WriteHeader(http.StatusOK)
	json.NewEncoder(rw).Encode(response)
}
