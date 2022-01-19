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
    "go.mongodb.org/mongo-driver/mongo/options"	
	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/configs"
	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/middleware"
)

var teamCollection *mongo.Collection = configs.GetCollection(configs.DB, "DEV_pokemon_teams_snapshots")

// TODO: middleware for getting teams by specific Pokemon

func GetAllTeams() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		log.Infof("`GetAllTeams`")
		// Configure header
		rw.Header().Set("content-type", "application/json")
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)

		// Query for all teams in reverse-chronological order
		findOptions := options.Find()
		page, limit := middleware.Pagination(r, findOptions)
		// TODO: Clean up logging messages
		log.Infof("Page: %d, Limit: %d", page, limit)
		findOptions.SetSort(bson.D{primitive.E{Key: "date", Value: -1}})
		cursor, err := teamCollection.Find(ctx, bson.M{}, findOptions)
		if err != nil {
			rw.WriteHeader(http.StatusInternalServerError)
            json.NewEncoder(rw).Encode(err.Error())
			return
		}
	
		defer cursor.Close(ctx)
		var snapshots []models.PokemonTeamsSnapshot
		for cursor.Next(ctx) {
			var snapshot models.PokemonTeamsSnapshot
			err := cursor.Decode(&snapshot)
			if err != nil {
				rw.WriteHeader(http.StatusInternalServerError)
				json.NewEncoder(rw).Encode(err.Error())
				return
			}
			snapshots = append(snapshots, snapshot)
		}
		if err := cursor.Err(); err != nil {
			rw.WriteHeader(http.StatusInternalServerError)
            json.NewEncoder(rw).Encode(err.Error())
			return
		}

		rw.WriteHeader(http.StatusOK)
		json.NewEncoder(rw).Encode(snapshots)
	}
}

// GetTeamsByFormat() /teams/{format}
func GetTeamsByFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		log.Infof("`GetTeamsByFormat`")
		// Configure header
		rw.Header().Set("content-type", "application/json")
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)

		// Get URL parameters
		urlParams := mux.Vars(r)
		format := urlParams["format"]
		fmt.Println(format)

		// Query for all teams in reverse-chronological order
		findOptions := options.Find()
		page, limit := middleware.Pagination(r, findOptions)
		log.Infof("Page: %d, Limit: %d", page, limit)
		findOptions.SetSort(bson.D{primitive.E{Key: "date", Value: -1}})
		cursor, err := teamCollection.Find(ctx, bson.M{"format_id": format}, findOptions)
		if err != nil {
			rw.WriteHeader(http.StatusInternalServerError)
            json.NewEncoder(rw).Encode(err.Error())
			return
		}
	
		defer cursor.Close(ctx)
		var snapshots []models.PokemonTeamsSnapshot
		for cursor.Next(ctx) {
			var snapshot models.PokemonTeamsSnapshot
			err := cursor.Decode(&snapshot)
			if err != nil {
				rw.WriteHeader(http.StatusInternalServerError)
				json.NewEncoder(rw).Encode(err.Error())
				return
			}
			snapshots = append(snapshots, snapshot)
		}
		if err := cursor.Err(); err != nil {
			rw.WriteHeader(http.StatusInternalServerError)
            json.NewEncoder(rw).Encode(err.Error())
			return
		}

		rw.WriteHeader(http.StatusOK)
		json.NewEncoder(rw).Encode(snapshots)
	}
}

// GetTeamsByFormatAndDate() /teams/{format}/{date}
func GetTeamsByFormatAndDate() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		log.Infof("`GetTeamsByFormatAndDate`")
		// Configure header
		rw.Header().Set("content-type", "application/json")
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)

		// Get URL parameters
		urlParams := mux.Vars(r)
		format := urlParams["format"]
		date := urlParams["date"]

		var snapshot models.PokemonTeamsSnapshot
		err := teamCollection.FindOne(ctx, bson.D{
			primitive.E{
				Key: "format_id", Value: format,
			}, 
			primitive.E{
				Key: "date", Value: date,
			},
		}).Decode(&snapshot)
		fmt.Println(snapshot)
		if err != nil {
			rw.WriteHeader(http.StatusInternalServerError)
            json.NewEncoder(rw).Encode(err.Error())
			return
		}
	
		rw.WriteHeader(http.StatusOK)
		json.NewEncoder(rw).Encode(snapshot)
	}
}
