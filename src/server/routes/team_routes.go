package routes

import (
	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/controllers"
)

func TeamRoute(router *mux.Router) {
	router.HandleFunc("/teams", controllers.GetAllTeams()).Methods("GET")
	router.HandleFunc("/teams/{format}", controllers.GetTeamsByFormat()).Methods("GET")
	router.HandleFunc("/teams/{format}/{date}", controllers.GetTeamsByFormatAndDate()).Methods("GET")
}
