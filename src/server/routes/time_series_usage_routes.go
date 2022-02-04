package routes

import (
	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/controllers"
)

// Configure router for time-series usage-related routes.
func TimeSeriesUsageRoute(router *mux.Router) {
	router.HandleFunc("/time-usage/{pokemon}", controllers.GetTimeSeriesUsageByPokemon()).Methods("GET")
	router.HandleFunc("/time-usage/{pokemon}/{format}", controllers.GetTimeSeriesUsageByPokemonFormat()).Methods("GET")
}
