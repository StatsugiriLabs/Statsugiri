package routes

import (
	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/controllers"
)

func TeamRoute(router *mux.Router) {
	router.HandleFunc("/teams", controllers.GetAllTeamSnapshots()).Methods("GET")
	router.HandleFunc("/teams/{format}", controllers.GetTeamSnapshotsByFormat()).Methods("GET")
	router.HandleFunc("/teams/{format}/{date}", controllers.GetTeamSnapshotsByFormatAndDate()).Methods("GET")
}
