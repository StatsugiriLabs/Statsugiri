package utils

import (
	"encoding/json"
	"io/ioutil"
	"os"

	log "github.com/sirupsen/logrus"
)

var FormatsRes map[string]interface{}

// Initialize constants from shared files
func init() {
	// Read JSON files
	jsonFile, err := os.Open("../shared/formats.json")
	if err != nil {
		log.Fatal(err)
	}
	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)
	err = json.Unmarshal(byteValue, &FormatsRes)
	if err != nil {
		log.Fatal(err)
	}
}
