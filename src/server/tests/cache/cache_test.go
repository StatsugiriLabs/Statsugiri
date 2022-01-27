package tests

import (
	"testing"
	"time"

	"github.com/kelvinkoon/babiri_v2/cache"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"go.mongodb.org/mongo-driver/bson"
)

const (
	TTL      = 60
	CAPACITY = 2
)

// Mock value for simulating time
var testNow int64

type mockScheduler struct {
	mock.Mock
	schedule func()
}

func (m *mockScheduler) CreateTicker(d time.Duration) <-chan time.Time {
	args := m.Called(d)
	return args.Get(0).(chan time.Time)
}

func (m *mockScheduler) Now() int64 {
	m.Called()
	return testNow
}

// Test cache insert and removal. Check stale eviction works.
func TestCacheGetPutHappyPathAndStaleEviction(t *testing.T) {
	assert := assert.New(t)
	compositeKey := "TestCompositeKey"
	expectedResult := []bson.M{{"TestResultKey": "TestResultValue"}}

	// Initialize scheduler
	scheduler := new(mockScheduler)
	evictChan := make(chan time.Time)
	scheduler.On("CreateTicker", time.Second).Return(evictChan)
	cache := cache.NewResponseCache(scheduler, CAPACITY)
	scheduler.On("Now").Return()

	// Test happy path get and put operations
	testNow = 0
	cache.Put(compositeKey, expectedResult)
	result, found := cache.Get(compositeKey)
	assert.True(found)
	assert.Equal(result, expectedResult)

	// Test cache has evicted entry after TTL
	testNow = TTL + 1
	evictChan <- time.Time{}
	time.Sleep(1 * time.Second)
	_, found = cache.Get(compositeKey)
	assert.False(found)
}

// Test cache put when full.
func TestCacheFullShouldNotWrite(t *testing.T) {
	assert := assert.New(t)
	compositeKey1 := "TestCompositeKey1"
	compositeKey2 := "TestCompositeKey2"
	compositeKey3 := "TestCompositeKey3"
	expectedResult1 := []bson.M{{"TestResultKey1": "TestResultValue1"}}
	expectedResult2 := []bson.M{{"TestResultKey2": "TestResultValue2"}}
	result3 := []bson.M{{"TestResultKey3": "TestResultValue3"}}

	// Initialize scheduler
	scheduler := new(mockScheduler)
	evictChan := make(chan time.Time)
	scheduler.On("CreateTicker", time.Second).Return(evictChan)
	cache := cache.NewResponseCache(scheduler, CAPACITY)
	scheduler.On("Now").Return()

	// Fill cache to capacity
	cache.Put(compositeKey1, expectedResult1)
	cache.Put(compositeKey2, expectedResult2)

	// Attempt to write to full cache
	cache.Put(compositeKey3, result3)

	// Verify no more writes were made
	result1, found1 := cache.Get(compositeKey1)
	result2, found2 := cache.Get(compositeKey2)
	assert.True(found1)
	assert.Equal(result1, expectedResult1)
	assert.True(found2)
	assert.Equal(result2, expectedResult2)

	// Verify additional entry was not written
	_, found3 := cache.Get(compositeKey3)
	assert.False(found3)
}
