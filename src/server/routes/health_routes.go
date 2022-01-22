package routes

import (
	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/controllers"
)

// Configure router for health-related routes.
func HealthRoute(router *mux.Router) {
	router.HandleFunc("/health", controllers.GetHealth()).Methods("GET")
}
