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

func getExpectedUsageSnapshots() string {
	jsonFile, err := os.Open("../assets/all_usage_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

func getExpectedUsageSnapshotsByFormat() string {
	jsonFile, err := os.Open("../assets/format_usage_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

func getExpectedUsageSnapshotsByFormatDate() string {
	jsonFile, err := os.Open("../assets/format_date_usage_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

// Test retrieving all usage snapshots.
func TestGetAllTeamSnapshotsHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetAllUsageSnapshots())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedUsageSnapshots())
}

// Test retrieving usage snapshots by format.
func TestGetUsageSnapshotsByFormatHappyPath(t *testing.T) {
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

	handler := http.HandlerFunc(controllers.GetUsageSnapshotsByFormat())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedUsageSnapshotsByFormat())
}

// Test retrieving usage snapshots by format and date.
func TestGetUsageSnapshotsByFormatDateHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format": "gen8vgc2021series11",
		"date":   "2022-01-25",
	}
	req = mux.SetURLVars(req, vars)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetUsageSnapshotsByFormatAndDate())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedUsageSnapshotsByFormatDate())
}
