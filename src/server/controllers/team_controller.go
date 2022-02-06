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
	"github.com/kelvinkoon/babiri_v2/models"
	"github.com/kelvinkoon/babiri_v2/transformers"
	log "github.com/sirupsen/logrus"
	"go.mongodb.org/mongo-driver/bson"
)

const (
	ALL_TEAMS_STR            = "AllTeams"
	TEAMS_BY_FORMAT_STR      = "TeamsByFormat"
	TEAMS_BY_FORMAT_DATE_STR = "TeamsByFormatDate"
	PAGINATION_LIMIT         = 5
)

// Returns handler for retrieving all team snapshots.
// Can filter teams by Pokémon query parameter.
func GetAllTeamSnapshots() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		skip, limit, err := middleware.ParsePagination(rw, r, PAGINATION_LIMIT)
		if err != nil {
			errors.CreateBadRequestErrorResponse(rw, err)
			return
		}
		pokemon := r.URL.Query().Get("pokemon")

		pipeline := utils.MakeTeamQueryPipeline(pokemon, []bson.M{})
		composite_key := utils.MakeCompositeKey(ALL_TEAMS_STR, pokemon)
		queryTeamsSnapshots(rw, pipeline, composite_key, skip, limit)
	}
}

// Returns handler for retrieving all team snapshots by format.
// Can filter teams by Pokémon query parameter.
func GetTeamSnapshotsByFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		skip, limit, err := middleware.ParsePagination(rw, r, PAGINATION_LIMIT)
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
		intermediateStages := []bson.M{
			// Match with format provided
			{
				"$match": bson.M{
					"FormatId": format,
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
		skip, limit, err := middleware.ParsePagination(rw, r, PAGINATION_LIMIT)
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
		if !utils.ValidDateFormat(date) {
			errors.CreateBadRequestErrorResponse(rw,
				fmt.Errorf("Date (%s) must match 'yyyy-mm-dd' format", date))
			return
		}
		pokemon := r.URL.Query().Get("pokemon")

		// Generate pipeline stages
		intermediateStages := []bson.M{
			// Match with format provided
			{
				"$match": bson.M{
					"FormatId": format,
				},
			},
			// Match with date provided
			{
				"$match": bson.M{
					"Date": date,
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
func queryTeamsSnapshots(rw http.ResponseWriter, pipeline []bson.M, composite_key string, skip int, limit int) {
	start := time.Now()

	var snapshots []models.PokemonTeamsSnapshot
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

		if err = cursor.All(ctx, &snapshots); err != nil {
			panic(err)
		}

		// Write to cache if results found
		if len(snapshots) != 0 {
			cache.C.Put(composite_key, snapshots)
		}
	}

	paginated_snapshots := utils.SliceTeamSnapshots(snapshots, skip, limit)
	response := transformers.TransformTeamSnapshotsToResponse(paginated_snapshots, skip, limit)

	log.Infof("%d results returned in %s", len(paginated_snapshots), time.Since(start))
	rw.WriteHeader(http.StatusOK)
	json.NewEncoder(rw).Encode(response)
}
