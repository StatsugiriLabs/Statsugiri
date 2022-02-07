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
	pipeline := utils.MakeUsageQueryPipeline(usageType, []bson.M{})
	queryUsageSnapshots(rw, pipeline, skip, limit, usageType)
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
	intermediateStages := []bson.M{
		// Match with format provided
		{
			"$match": bson.M{
				"FormatId": format,
			},
		},
	}

	pipeline := utils.MakeUsageQueryPipeline(usageType, intermediateStages)
	queryUsageSnapshots(rw, pipeline, skip, limit, usageType)
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

	pipeline := utils.MakeUsageQueryPipeline(usageType, intermediateStages)
	queryUsageSnapshots(rw, pipeline, skip, limit, usageType)
}

// Queries usage collection using aggregation pipeline and encode results.
// Writes to cache if results found.
func queryUsageSnapshots(rw http.ResponseWriter, pipeline []bson.M, skip int, limit int, usage utils.UsageType) {
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

	// Iterate through query results
	if err = cursor.All(ctx, &snapshots); err != nil {
		panic(err)
	}

	// Paginate snapshot results
	paginated_snapshots := utils.SliceUsageSnapshots(snapshots, skip, limit)

	// Write results to response
	writeUsageResponse(rw, paginated_snapshots, skip, limit, usage)
	log.Infof("%d results returned in %s", len(paginated_snapshots), time.Since(start))
}

// Transform internal models to response models and write to usage response depending on usage type.
func writeUsageResponse(rw http.ResponseWriter, snapshots []models.PokemonUsageSnapshot, skip int, limit int, usage utils.UsageType) {
	switch usage {
	case utils.Usage:
		response := transformers.TransformUsageSnapshotsToUsageResponse(snapshots, skip, limit)
		rw.WriteHeader(http.StatusOK)
		json.NewEncoder(rw).Encode(response)
	case utils.RatingUsage:
		response := transformers.TransformRatingUsageSnapshotsToRatingUsageResponse(snapshots, skip, limit)
		rw.WriteHeader(http.StatusOK)
		json.NewEncoder(rw).Encode(response)
	case utils.PartnerUsage:
		response := transformers.TransformPartnerUsageSnapshotsToPartnerUsageResponse(snapshots, skip, limit)
		rw.WriteHeader(http.StatusOK)
		json.NewEncoder(rw).Encode(response)
	default:
		// TODO: Add an actual error message
		errors.CreateInternalServerErrorResponse(rw, nil)
	}
}
