package routes

import (
	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/controllers"
)

// Configure router for team-related routes.
func TeamRoute(router *mux.Router) {
	router.HandleFunc("/api/teams", controllers.GetAllTeamSnapshots()).Methods("GET")
	router.HandleFunc("/api/teams/{format}", controllers.GetTeamSnapshotsByFormat()).Methods("GET")
	router.HandleFunc("/api/teams/{format}/{date}", controllers.GetTeamSnapshotsByFormatAndDate()).Methods("GET")
}
