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

func getExpectedRatingUsageSnapshots() string {
	jsonFile, err := os.Open("../assets/all_rating_usage_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

func getExpectedPartnerUsageSnapshots() string {
	jsonFile, err := os.Open("../assets/all_partner_usage_snapshots_test_res.txt")
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

func getExpectedRatingUsageSnapshotsByFormat() string {
	jsonFile, err := os.Open("../assets/format_rating_usage_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

func getExpectedPartnerUsageSnapshotsByFormat() string {
	jsonFile, err := os.Open("../assets/format_partner_usage_snapshots_test_res.txt")
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

func getExpectedRatingUsageSnapshotsByFormatDate() string {
	jsonFile, err := os.Open("../assets/format_date_rating_usage_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

func getExpectedPartnerUsageSnapshotsByFormatDate() string {
	jsonFile, err := os.Open("../assets/format_date_partner_usage_snapshots_test_res.txt")
	result, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	return string(result)
}

// Test retrieving all usage snapshots.
func TestGetAllUsageSnapshotsHappyPath(t *testing.T) {
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

// Test retrieving all rating usage snapshots.
func TestGetAllRatingUsageSnapshotsHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetAllRatingUsageSnapshots())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedRatingUsageSnapshots())
}

// Test retrieving all partner usage snapshots.
func TestGetAllPartnerUsageSnapshotsHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetAllPartnerUsageSnapshots())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedPartnerUsageSnapshots())
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

// Test retrieving rating usage snapshots by format.
func TestGetRatingUsageSnapshotsByFormatHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format": "gen8ou",
	}
	req = mux.SetURLVars(req, vars)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetRatingUsageSnapshotsByFormat())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedRatingUsageSnapshotsByFormat())
}

// Test retrieving partner usage snapshots by format.
func TestGetPartnerUsageSnapshotsByFormatHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format": "gen8ou",
	}
	req = mux.SetURLVars(req, vars)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetPartnerUsageSnapshotsByFormat())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedPartnerUsageSnapshotsByFormat())
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

// Test retrieving rating usage snapshots by format and date.
func TestGetRatingUsageSnapshotsByFormatDateHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format": "gen8ou",
		"date":   "2022-01-25",
	}
	req = mux.SetURLVars(req, vars)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetRatingUsageSnapshotsByFormatAndDate())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedRatingUsageSnapshotsByFormatDate())
}

// Test retrieving partner usage snapshots by format and date.
func TestGetPartnerUsageSnapshotsByFormatDateHappyPath(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format": "gen8ou",
		"date":   "2022-01-26",
	}
	req = mux.SetURLVars(req, vars)

	// Set query params
	q := req.URL.Query()
	q.Add("page", "1")
	q.Add("limit", "5")
	req.URL.RawQuery = q.Encode()

	handler := http.HandlerFunc(controllers.GetPartnerUsageSnapshotsByFormatAndDate())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusOK)
	// Check response body
	assert.Equal(t, string(body), getExpectedPartnerUsageSnapshotsByFormatDate())
}

// Test providing an invalid format to endpoint.
func TestGetUsageSnapshotsByFormatInvalidFormat(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params
	vars := map[string]string{
		"format": "not_a_real_format",
	}
	req = mux.SetURLVars(req, vars)

	handler := http.HandlerFunc(controllers.GetUsageSnapshotsByFormat())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusBadRequest)
	assert.Equal(t, string(body), "{\"error\":\"Format (not_a_real_format) is not supported\"}\n")
}

// Test providing an invalid date to endpoint.
func TestGetUsageSnapshotsByFormatDateInvalidDate(t *testing.T) {
	rr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)

	// Set URL params with invalid date
	vars := map[string]string{
		"format": "gen8ou",
		"date":   "2021-1-31",
	}
	req = mux.SetURLVars(req, vars)

	handler := http.HandlerFunc(controllers.GetUsageSnapshotsByFormatAndDate())
	handler.ServeHTTP(rr, req)
	body, err := io.ReadAll(rr.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Check status code
	assert.Equal(t, rr.Code, http.StatusBadRequest)
	assert.Equal(t, string(body), "{\"error\":\"Date (2021-1-31) must match 'yyyy-mm-dd' format\"}\n")
}
