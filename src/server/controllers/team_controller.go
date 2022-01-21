package controllers

import (
	"context"
	log "github.com/sirupsen/logrus"
	"encoding/json"
	"net/http"
	"time"
	"fmt"
	"go.mongodb.org/mongo-driver/bson/primitive"
    "go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/bson"
	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/configs"
	"github.com/kelvinkoon/babiri_v2/middleware"
	"github.com/kelvinkoon/babiri_v2/utils"
)

var teamCollection *mongo.Collection = configs.GetCollection(configs.DB, "DEV_pokemon_teams_snapshots")

func GetAllTeamSnapshots() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		log.Infof("`GetAllTeamsSnapshots`")

		// Get parameters and pagination options
		page, limit := middleware.ParsePagination(r)
		pokemon := r.URL.Query().Get("pokemon")

		// Generate pipeline stages
		var intermediateStages []bson.D

		pipeline := MakeTeamQueryPipeline(page, limit, pokemon, intermediateStages)
		queryTeamsSnapshots(rw, pipeline)
	}
}

// GetTeamsSnapshotsByFormat() /teams/{format}
func GetTeamSnapshotsByFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		log.Infof("`GetTeamsSnapshotsByFormat`")

		// Get parameters and pagination options
		page, limit := middleware.ParsePagination(r)
		format := mux.Vars(r)["format"]
		pokemon := r.URL.Query().Get("pokemon")

		// Generate pipeline stages
		intermediateStages := []bson.D{
			// Match with format provided
			bson.D{
				primitive.E{
					Key: "$match", Value: bson.D{
						primitive.E{
							Key: "format_id", Value: format,
						},
					},
				},
			},
		}

		pipeline := MakeTeamQueryPipeline(page, limit, pokemon, intermediateStages)
		queryTeamsSnapshots(rw, pipeline)
	}
}

// GetTeamsSnapshotsByFormatAndDate() /teams/{format}/{date}
func GetTeamSnapshotsByFormatAndDate() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		log.Infof("`GetTeamsSnapshotsByFormatAndDate`")

		// Get parameters and pagination options
		page, limit := middleware.ParsePagination(r)
		format := mux.Vars(r)["format"]
		date := mux.Vars(r)["date"]
		pokemon := r.URL.Query().Get("pokemon")

		// Generate pipeline stages
		intermediateStages := []bson.D{
			// Match with format provided
			bson.D{
				primitive.E{
					Key: "$match", Value: bson.D{
						primitive.E{
							Key: "format_id", Value: format,
						},
					},
				},
			},
			// Match with date provided
			bson.D{
				primitive.E{
					Key: "$match", Value: bson.D{
						primitive.E{
							Key: "date", Value: date,
						},
					},
				},
			},
		}

		pipeline := MakeTeamQueryPipeline(page, limit, pokemon, intermediateStages)
		queryTeamsSnapshots(rw, pipeline)
	}
}


func queryTeamsSnapshots(rw http.ResponseWriter, pipeline mongo.Pipeline) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Run query with options
	cursor, err := teamCollection.Aggregate(ctx, pipeline)
	if err != nil {
		utils.CreateInternalServerErrorResponse(rw, err)
		return
	}
	defer cursor.Close(ctx)

	// Iterate through queries 
	var snapshots []bson.M
	if err = cursor.All(ctx, &snapshots); err != nil {
		panic(err)
	}
	fmt.Println(snapshots)
	fmt.Println(len(snapshots))

	rw.WriteHeader(http.StatusOK)
	json.NewEncoder(rw).Encode(snapshots)	
}
