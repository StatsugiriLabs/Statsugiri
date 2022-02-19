package routes

import (
	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/controllers"
)

// Configure router for usage-related routes.
func UsageRoute(router *mux.Router) {
	router.HandleFunc("/api/usage", controllers.GetAllUsageSnapshots()).Methods("GET")
	router.HandleFunc("/api/usage/{format}", controllers.GetUsageSnapshotsByFormat()).Methods("GET")
	router.HandleFunc("/api/usage/{format}/{date}", controllers.GetUsageSnapshotsByFormatAndDate()).Methods("GET")
	router.HandleFunc("/api/rating-usage", controllers.GetAllRatingUsageSnapshots()).Methods("GET")
	router.HandleFunc("/api/rating-usage/{format}", controllers.GetRatingUsageSnapshotsByFormat()).Methods("GET")
	router.HandleFunc("/api/rating-usage/{format}/{date}", controllers.GetRatingUsageSnapshotsByFormatAndDate()).Methods("GET")
	router.HandleFunc("/api/partner-usage", controllers.GetAllPartnerUsageSnapshots()).Methods("GET")
	router.HandleFunc("/api/partner-usage/{format}", controllers.GetPartnerUsageSnapshotsByFormat()).Methods("GET")
	router.HandleFunc("/api/partner-usage/{format}/{date}", controllers.GetPartnerUsageSnapshotsByFormatAndDate()).Methods("GET")
}
