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
