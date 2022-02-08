package tests

import (
	"io"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	"github.com/gorilla/mux"
	"github.com/kelvinkoon/babiri_v2/controllers"
	log "github.com/sirupsen/logrus"

	"github.com/stretchr/testify/assert"
)

func getExpectedTimeSeriesSnapshots() string {
	jsonFile, err := os.Open("../assets/pokemon_time_series_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

func getExpectedFormatTimeSeriesSnapshots() string {
	jsonFile, err := os.Open("../assets/pokemon_format_time_series_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

// Test retrieving time series snapshots by Pokémon.
func TestGetPokemonTimeSeriesSnapshotsHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"pokemon": "Landorus-Therian",
	}
	req = mux.SetURLVars(req, vars)

	handler := http.HandlerFunc(controllers.GetTimeSeriesUsageByPokemon())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedTimeSeriesSnapshots())
}

// Test retrieving time series snapshots by Pokémon and format.
func TestGetPokemonFormatTimeSeriesSnapshotsHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format":  "gen8vgc2021series11",
		"pokemon": "Landorus-Therian",
	}
	req = mux.SetURLVars(req, vars)

	handler := http.HandlerFunc(controllers.GetTimeSeriesUsageByPokemonFormat())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedFormatTimeSeriesSnapshots())
}

// Test retrieving time series snapshots using invalid format.
func TestGetPokemonFormatTimeSeriesSnapshotsInvalidFormat(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format":  "not_a_real_format",
		"pokemon": "Landorus-Therian",
	}
	req = mux.SetURLVars(req, vars)

	handler := http.HandlerFunc(controllers.GetTimeSeriesUsageByPokemonFormat())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusBadRequest)
	assert.Equal(t, string(body), "{\"error\":\"Format (not_a_real_format) is not supported\"}\n")
}
