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
	"github.com/kelvinkoon/babiri_v2/transformers"
	log "github.com/sirupsen/logrus"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

func GetTimeSeriesUsageByPokemon() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// TODO: https://github.com/kelvinkoon/babiri_v2/issues/112
		pokemon := mux.Vars(r)["pokemon"]

		// Generate pipeline stages
		intermediateStages := []bson.D{}

		pipeline := utils.MakeTimeSeriesUsageQueryPipeline(pokemon, intermediateStages)
		queryTimeSeriesData(rw, pipeline, pokemon)
	}
}

func GetTimeSeriesUsageByPokemonFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// TODO: https://github.com/kelvinkoon/babiri_v2/issues/112
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
