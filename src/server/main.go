package main

import (
	"net/http"

	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/db"
	"github.com/kelvinkoon/babiri_v2/middleware"
	"github.com/kelvinkoon/babiri_v2/routes"
	log "github.com/sirupsen/logrus"
)

func main() {
	// Configure router
	router := mux.NewRouter()
	router.Use(middleware.HeaderMiddleware)

	// Connect to database
	db.ConnectDB()

	// Configure routes
	routes.HealthRoute(router)
	routes.FormatRoute(router)
	routes.TeamRoute(router)
	routes.UsageRoute(router)
	routes.TimeSeriesUsageRoute(router)

	log.Infof("Server running on Port 3000")
	log.Fatal(http.ListenAndServe(":3000", router))
}
