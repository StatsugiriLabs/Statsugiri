package main

import (
	"net/http"

	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/configs"
	"github.com/kelvinkoon/babiri_v2/middleware"
	"github.com/kelvinkoon/babiri_v2/routes"
	log "github.com/sirupsen/logrus"
)

func main() {
	// Configure router
	router := mux.NewRouter()
	router.Use(middleware.HeaderMiddleware)

	// Connect to database
	configs.ConnectDB()

	// Configure routes
	routes.TeamRoute(router)
	routes.FormatRoute(router)
	routes.HealthRoute(router)

	log.Fatal(http.ListenAndServe(":3000", router))
}
