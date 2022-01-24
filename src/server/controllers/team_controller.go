package controllers

import (
	"context"
	"encoding/json"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/configs"
	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	"github.com/kelvinkoon/babiri_v2/errors"
	"github.com/kelvinkoon/babiri_v2/middleware"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

var teamCollection *mongo.Collection = configs.GetCollection(configs.DB, utils.PokemonTeamSnapshotsCollectionName)

// Returns handler for retrieving all team snapshots.
// Can filter teams by Pokémon query parameter.
func GetAllTeamSnapshots() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		page, limit := middleware.ParsePagination(r)
		pokemon := r.URL.Query().Get("pokemon")

		// Generate pipeline stages
		var intermediateStages []bson.D

		pipeline := utils.MakeTeamQueryPipeline(page, limit, pokemon, intermediateStages)
		queryTeamsSnapshots(rw, pipeline)
	}
}

// Returns handler for retrieving all team snapshots by format.
// Can filter teams by Pokémon query parameter.
func GetTeamSnapshotsByFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		page, limit := middleware.ParsePagination(r)
		format := mux.Vars(r)["format"]
		pokemon := r.URL.Query().Get("pokemon")

		// Generate pipeline stages
		intermediateStages := []bson.D{
			// Match with format provided
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

		pipeline := utils.MakeTeamQueryPipeline(page, limit, pokemon, intermediateStages)
		queryTeamsSnapshots(rw, pipeline)
	}
}

// Returns handler for retrieving all team snapshots by format and date.
// Can filter teams by Pokémon query parameter.
func GetTeamSnapshotsByFormatAndDate() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		page, limit := middleware.ParsePagination(r)
		format := mux.Vars(r)["format"]
		date := mux.Vars(r)["date"]
		pokemon := r.URL.Query().Get("pokemon")

		// Generate pipeline stages
		intermediateStages := []bson.D{
			// Match with format provided
			{
				primitive.E{
					Key: "$match", Value: bson.D{
						primitive.E{
							Key: "FormatId", Value: format,
						},
					},
				},
			},
			// Match with date provided
			{
				primitive.E{
					Key: "$match", Value: bson.D{
						primitive.E{
							Key: "Date", Value: date,
						},
					},
				},
			},
		}

		pipeline := utils.MakeTeamQueryPipeline(page, limit, pokemon, intermediateStages)
		queryTeamsSnapshots(rw, pipeline)
	}
}

// Encodes the response with snapshot results from aggregation pipeline.
func queryTeamsSnapshots(rw http.ResponseWriter, pipeline mongo.Pipeline) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Run query with options
	cursor, err := teamCollection.Aggregate(ctx, pipeline)
	if err != nil {
		errors.CreateInternalServerErrorResponse(rw, err)
		return
	}
	defer cursor.Close(ctx)

	// Iterate through queries
	var snapshots []bson.M
	if err = cursor.All(ctx, &snapshots); err != nil {
		panic(err)
	}

	rw.WriteHeader(http.StatusOK)
	json.NewEncoder(rw).Encode(snapshots)
}
