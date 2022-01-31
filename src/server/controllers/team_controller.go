package controllers

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/cache"
	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	db "github.com/kelvinkoon/babiri_v2/db"
	"github.com/kelvinkoon/babiri_v2/errors"
	"github.com/kelvinkoon/babiri_v2/middleware"
	log "github.com/sirupsen/logrus"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

const (
	ALL_TEAMS_STR            = "AllTeams"
	TEAMS_BY_FORMAT_STR      = "TeamsByFormat"
	TEAMS_BY_FORMAT_DATE_STR = "TeamsByFormatDate"
)

// Returns handler for retrieving all team snapshots.
// Can filter teams by Pokémon query parameter.
func GetAllTeamSnapshots() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		skip, limit, err := middleware.ParsePagination(rw, r)
		if err != nil {
			errors.CreateBadRequestErrorResponse(rw, err)
			return
		}
		pokemon := r.URL.Query().Get("pokemon")

		pipeline := utils.MakeTeamQueryPipeline(pokemon, []bson.D{})
		composite_key := utils.MakeCompositeKey(ALL_TEAMS_STR, pokemon)
		queryTeamsSnapshots(rw, pipeline, composite_key, skip, limit)
	}
}

// Returns handler for retrieving all team snapshots by format.
// Can filter teams by Pokémon query parameter.
func GetTeamSnapshotsByFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		skip, limit, err := middleware.ParsePagination(rw, r)
		if err != nil {
			errors.CreateBadRequestErrorResponse(rw, err)
			return
		}
		format := mux.Vars(r)["format"]
		if !utils.ValidFormat(format) {
			errors.CreateBadRequestErrorResponse(rw,
				fmt.Errorf("Format (%s) is not supported", format))
			return
		}

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

		pipeline := utils.MakeTeamQueryPipeline(pokemon, intermediateStages)
		composite_key := utils.MakeCompositeKey(TEAMS_BY_FORMAT_STR, format, pokemon)
		queryTeamsSnapshots(rw, pipeline, composite_key, skip, limit)
	}
}

// Returns handler for retrieving all team snapshots by format and date.
// Can filter teams by Pokémon query parameter.
func GetTeamSnapshotsByFormatAndDate() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		skip, limit, err := middleware.ParsePagination(rw, r)
		if err != nil {
			errors.CreateBadRequestErrorResponse(rw, err)
			return
		}
		format := mux.Vars(r)["format"]
		if !utils.ValidFormat(format) {
			errors.CreateBadRequestErrorResponse(rw,
				fmt.Errorf("Format (%s) is not supported", format))
			return
		}
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

		pipeline := utils.MakeTeamQueryPipeline(pokemon, intermediateStages)
		composite_key := utils.MakeCompositeKey(TEAMS_BY_FORMAT_DATE_STR, format, date, pokemon)
		queryTeamsSnapshots(rw, pipeline, composite_key, skip, limit)
	}
}

// Queries collection using aggregation pipeline and encode results.
// Writes to cache if results found.
func queryTeamsSnapshots(rw http.ResponseWriter, pipeline mongo.Pipeline, composite_key string, skip int, limit int) {
	start := time.Now()

	var snapshots []bson.M
	var found bool

	// Send request if cache is not hit
	if snapshots, found = cache.C.Get(composite_key); !found {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		// Run query with pipeline
		cursor, err := db.TeamCollection.Aggregate(ctx, pipeline)
		if err != nil {
			errors.CreateInternalServerErrorResponse(rw, err)
			return
		}
		defer cursor.Close(ctx)

		// Iterate through query results
		if err = cursor.All(ctx, &snapshots); err != nil {
			panic(err)
		}

		// Write to cache if results found
		if len(snapshots) != 0 {
			cache.C.Put(composite_key, snapshots)
		}
	}
	// Paginate snapshot results
	paginated_snapshots := utils.SliceResults(snapshots, skip, limit)

	log.Infof("%d results returned in %s", len(paginated_snapshots), time.Since(start))
	rw.WriteHeader(http.StatusOK)
	json.NewEncoder(rw).Encode(paginated_snapshots)
}
