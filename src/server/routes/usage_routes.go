package routes

import (
	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/controllers"
)

// Configure router for usage-related routes.
func UsageRoute(router *mux.Router) {
	router.HandleFunc("/usage", controllers.GetAllUsageSnapshots()).Methods("GET")
	router.HandleFunc("/usage/{format}", controllers.GetUsageSnapshotsByFormat()).Methods("GET")
	router.HandleFunc("/usage/{format}/{date}", controllers.GetUsageSnapshotsByFormatAndDate()).Methods("GET")
	router.HandleFunc("/rating-usage", controllers.GetAllRatingUsageSnapshots()).Methods("GET")
	router.HandleFunc("/rating-usage/{format}", controllers.GetRatingUsageSnapshotsByFormat()).Methods("GET")
	router.HandleFunc("/rating-usage/{format}/{date}", controllers.GetRatingUsageSnapshotsByFormatAndDate()).Methods("GET")
	router.HandleFunc("/partner-usage", controllers.GetAllPartnerUsageSnapshots()).Methods("GET")
	router.HandleFunc("/partner-usage/{format}", controllers.GetPartnerUsageSnapshotsByFormat()).Methods("GET")
	router.HandleFunc("/partner-usage/{format}/{date}", controllers.GetPartnerUsageSnapshotsByFormatAndDate()).Methods("GET")
}
