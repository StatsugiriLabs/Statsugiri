package main

import (
	"net/http"

	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/db"
	"github.com/kelvinkoon/babiri_v2/middleware"
	"github.com/kelvinkoon/babiri_v2/routes"
	log "github.com/sirupsen/logrus"
)

const Port = "3000"

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

	log.Infof("Server running on Port %s", Port)
	log.Fatal(http.ListenAndServe(":"+Port, router))
}
