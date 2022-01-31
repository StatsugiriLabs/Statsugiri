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

func getExpectedTeamSnapshotsFirstPage() string {
	jsonFile, err := os.Open("../assets/all_team_snapshots_test_res_page1.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

func getExpectedTeamSnapshotsSecondPage() string {
	jsonFile, err := os.Open("../assets/all_team_snapshots_test_res_page2.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

func getExpectedFormatTeamSnapshots() string {
	jsonFile, err := os.Open("../assets/format_team_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

func getExpectedFormatAndDateTeamSnapshots() string {
	jsonFile, err := os.Open("../assets/format_date_team_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

// Test retrieving all team snapshots for 1st page.
func TestGetAllTeamSnapshotsFirstPage(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetAllTeamSnapshots())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedTeamSnapshotsFirstPage())
}

// Test retrieving all team snapshots for arbitrary page (ie. 2nd page).
func TestGetAllTeamSnapshotsSecondPage(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "2")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetAllTeamSnapshots())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedTeamSnapshotsSecondPage())
}

// Test retrieving all team snapshots for a format.
func TestGetTeamSnapshotsByFormatHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format": "gen8vgc2021series11",
	}
	req = mux.SetURLVars(req, vars)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetTeamSnapshotsByFormat())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedFormatTeamSnapshots())
}

// Test retrieving all team snapshots for a format and date.
func TestGetTeamSnapshotsByFormatAndDateHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format": "gen8vgc2021series11",
		"date":   "2022-01-26",
	}
	req = mux.SetURLVars(req, vars)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetTeamSnapshotsByFormatAndDate())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedFormatAndDateTeamSnapshots())
}

// Test providing an invalid format to endpoint.
func TestGetTeamSnapshotsByFormatInvalidFormat(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format": "not_a_real_format",
	}
	req = mux.SetURLVars(req, vars)

	handler := http.HandlerFunc(controllers.GetTeamSnapshotsByFormat())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusBadRequest)
	assert.Equal(t, string(body), "{\"error\":\"Format (not_a_real_format) is not supported\"}\n")
}
