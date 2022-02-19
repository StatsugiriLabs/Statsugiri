package routes

import (
	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/controllers"
)

// Configure router for format-related routes.
func FormatRoute(router *mux.Router) {
	router.HandleFunc("/api/formats", controllers.GetFormats()).Methods("GET")
}
