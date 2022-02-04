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
	ALL_GENERIC_USAGE_STR            = "AllUsage"
	GENERIC_USAGE_BY_FORMAT_STR      = "UsageByFormat"
	GENERIC_USAGE_BY_FORMAT_DATE_STR = "UsageByFormatDate"
)

// Handlers for router

// Returns handler for retrieving all usage snapshots.
func GetAllUsageSnapshots() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		handleAllGenericUsageSnapshotsParams(rw, r, utils.Usage)
	}
}

// Returns handler for retrieving all rating usage snapshots.
func GetAllRatingUsageSnapshots() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		handleAllGenericUsageSnapshotsParams(rw, r, utils.RatingUsage)
	}
}

// Returns handler for retrieving all partner usage snapshots.
func GetAllPartnerUsageSnapshots() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		handleAllGenericUsageSnapshotsParams(rw, r, utils.PartnerUsage)
	}
}

// Returns handler for retrieving usage snapshots by format.
func GetUsageSnapshotsByFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		handleGenericUsageSnapshotsByFormatParams(rw, r, utils.Usage)
	}
}

// Returns handler for retrieving rating usage snapshots by format.
func GetRatingUsageSnapshotsByFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		handleGenericUsageSnapshotsByFormatParams(rw, r, utils.RatingUsage)
	}
}

// Returns handler for retrieving partner usage snapshots by format.
func GetPartnerUsageSnapshotsByFormat() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		handleGenericUsageSnapshotsByFormatParams(rw, r, utils.PartnerUsage)
	}
}

// Returns handler for retrieving usage snapshots by format and date.
func GetUsageSnapshotsByFormatAndDate() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		handleGenericUsageSnapshotsByFormatAndDateParams(rw, r, utils.Usage)
	}
}

// Returns handler for retrieving rating usage snapshots by format and date.
func GetRatingUsageSnapshotsByFormatAndDate() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		handleGenericUsageSnapshotsByFormatAndDateParams(rw, r, utils.RatingUsage)
	}
}

// Returns handler for retrieving partner usage snapshots by format and date.
func GetPartnerUsageSnapshotsByFormatAndDate() http.HandlerFunc {
	return func(rw http.ResponseWriter, r *http.Request) {
		handleGenericUsageSnapshotsByFormatAndDateParams(rw, r, utils.PartnerUsage)
	}
}

// Handles generating parameters such as pagination and pipeline stages for retrieving all usage snapshots.
func handleAllGenericUsageSnapshotsParams(rw http.ResponseWriter, r *http.Request, usageType utils.UsageType) {
	// Get parameters and pagination options
	skip, limit, err := middleware.ParsePagination(rw, r, utils.UsageLimit)
	if err != nil {
		errors.CreateBadRequestErrorResponse(rw, err)
		return
	}
	pipeline := utils.MakeUsageQueryPipeline(usageType, []bson.D{})
	composite_key := utils.MakeCompositeKey(ALL_GENERIC_USAGE_STR, usageType.String())
	queryUsageSnapshots(rw, pipeline, composite_key, skip, limit)
}

// Handles generating parameters such as pagination and pipeline stages for retrieving usage snapshots by format.
func handleGenericUsageSnapshotsByFormatParams(rw http.ResponseWriter, r *http.Request, usageType utils.UsageType) {
	// Get parameters and pagination options
	skip, limit, err := middleware.ParsePagination(rw, r, utils.UsageLimit)
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

	pipeline := utils.MakeUsageQueryPipeline(usageType, intermediateStages)
	composite_key := utils.MakeCompositeKey(GENERIC_USAGE_BY_FORMAT_STR, usageType.String(), format)
	queryUsageSnapshots(rw, pipeline, composite_key, skip, limit)
}

// Handles generating parameters such as pagination and pipeline stages for retrieving usage snapshots by format and date.
func handleGenericUsageSnapshotsByFormatAndDateParams(rw http.ResponseWriter, r *http.Request, usageType utils.UsageType) {
	// Get parameters and pagination options
	skip, limit, err := middleware.ParsePagination(rw, r, utils.UsageLimit)
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

	pipeline := utils.MakeUsageQueryPipeline(usageType, intermediateStages)
	composite_key := utils.MakeCompositeKey(GENERIC_USAGE_BY_FORMAT_DATE_STR, usageType.String(), format, date)
	queryUsageSnapshots(rw, pipeline, composite_key, skip, limit)
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
