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
	USAGE_LIMIT              = 10
	ALL_USAGE_STR            = "AllUsage"
	USAGE_BY_FORMAT_STR      = "UsageByFormat"
	USAGE_BY_FORMAT_DATE_STR = "UsageByFormatDate"
)

// Returns handler for retrieving all usage snapshots.
func GetAllUsageSnapshots() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		skip, limit, err := middleware.ParsePagination(rw, r, USAGE_LIMIT)
		if err != nil {
			errors.CreateBadRequestErrorResponse(rw, err)
			return
		}

		pipeline := utils.MakeUsageQueryPipeline(utils.Usage, []bson.D{})
		composite_key := utils.MakeCompositeKey(ALL_USAGE_STR)
		queryUsageSnapshots(rw, pipeline, composite_key, skip, limit)
	}
}

// Returns handler for retrieving all usage snapshots by format.
func GetUsageSnapshotsByFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		skip, limit, err := middleware.ParsePagination(rw, r, USAGE_LIMIT)
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

		pipeline := utils.MakeUsageQueryPipeline(utils.Usage, intermediateStages)
		composite_key := utils.MakeCompositeKey(USAGE_BY_FORMAT_STR, format)
		queryUsageSnapshots(rw, pipeline, composite_key, skip, limit)
	}
}

// Returns handler for retrieving all usage snapshots by format and date.
func GetUsageSnapshotsByFormatAndDate() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		// Get parameters and pagination options
		skip, limit, err := middleware.ParsePagination(rw, r, USAGE_LIMIT)
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

		pipeline := utils.MakeUsageQueryPipeline(utils.Usage, intermediateStages)
		composite_key := utils.MakeCompositeKey(USAGE_BY_FORMAT_DATE_STR, format)
		queryUsageSnapshots(rw, pipeline, composite_key, skip, limit)
	}
}

// Queries usage collection using aggregation pipeline and encode results.
// Writes to cache if results found.
func queryUsageSnapshots(rw http.ResponseWriter, pipeline mongo.Pipeline, composite_key string, skip int, limit int) {
	start := time.Now()

	var snapshots []bson.M
	var found bool

	// Send request if cache is not hit
	if snapshots, found = cache.C.Get(composite_key); !found {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		// Run query with pipeline
		cursor, err := db.UsageCollection.Aggregate(ctx, pipeline)
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
