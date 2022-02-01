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
	// router.HandleFunc("/rating-usage", controllers.GetAllUsageSnapshots()).Methods("GET")
	// router.HandleFunc("/partners-usage", controllers.GetAllUsageSnapshots()).Methods("GET")
	// router.HandleFunc("/time-usage", controllers.GetAllUsageSnapshots()).Methods("GET")
}
