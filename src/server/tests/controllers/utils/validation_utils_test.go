package tests

import (
	"testing"

	"github.com/kelvinkoon/babiri_v2/controllers/utils"
	"github.com/stretchr/testify/assert"
)

// Test when valid format provided.
func TestValidFormatHappyPath(t *testing.T) {
	assert.True(t, utils.ValidFormat("gen8ou"))
}

// Test when invalid format provided.
func TestValidFormatInvalidFormat(t *testing.T) {
	assert.False(t, utils.ValidFormat("not_a_real_format"))
}

// Test when valid date provided.
func TestValidDateHappyPath(t *testing.T) {
	assert.True(t, utils.ValidDateFormat("2021-12-31"))
}

// Test when invalid date provided by incorrect format without leading 0.
func TestInvalidDateNoLeadingZero(t *testing.T) {
	assert.False(t, utils.ValidDateFormat("2021-1-31"))
}

// Test when invalid date provided by incorrect format with extra characters.
func TestInvalidDateExtraChars(t *testing.T) {
	assert.False(t, utils.ValidDateFormat("2021-12-031"))
}
