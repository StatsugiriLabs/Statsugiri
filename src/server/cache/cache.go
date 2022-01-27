package cache

import (
	"sync"
	"time"

	log "github.com/sirupsen/logrus"
	"go.mongodb.org/mongo-driver/bson"
)

const (
	TTL = 60 // Cache entry lifetime from last access (seconds)
)

type CacheEntry struct {
	response   []bson.M
	lastAccess int64
}

type ResponseCache struct {
	// Let map key be compositeKey
	cacheMap  map[string]*CacheEntry
	rwLock    *sync.RWMutex
	scheduler SchedulerInterface
	capacity  int
}

// Start daemon for evicting expired cache entries.
func (c *ResponseCache) startEvictionDaemon() {
	ticker := c.scheduler.CreateTicker(time.Second)
	log.Infof("Starting eviction daemon")
	go func() {
		for {
			<-ticker
			c.evictCacheEntry()
		}
	}()
}

// Evict cache entry.
func (c *ResponseCache) evictCacheEntry() {
	c.rwLock.Lock()
	defer c.rwLock.Unlock()

	now := c.scheduler.Now()

	for compositeKey, cacheEntry := range c.cacheMap {
		if now-cacheEntry.lastAccess > int64(TTL) {
			_, exists := c.cacheMap[compositeKey]
			if exists {
				delete(c.cacheMap, compositeKey)
			}
		}
	}
}

// Check if cache is full denoted by MAX_ENTRIES.
func (c *ResponseCache) isCacheFull() bool {
	if len(c.cacheMap) >= c.capacity {
		return true
	}
	return false
}

// Put entry into cache given composite key and response.
func (c *ResponseCache) Put(compositeKey string, response []bson.M) {
	c.rwLock.Lock()
	defer c.rwLock.Unlock()

	// Write if cache is not full
	if !c.isCacheFull() {
		_, found := c.cacheMap[compositeKey]
		if !found {
			cacheEntry := &CacheEntry{
				response:   response,
				lastAccess: c.scheduler.Now(),
			}
			c.cacheMap[compositeKey] = cacheEntry
		}
	}
}

// Retrieve cache entry given composite key. If found, update last access time.
func (c *ResponseCache) Get(compositeKey string) ([]bson.M, bool) {
	c.rwLock.Lock()
	defer c.rwLock.Unlock()

	cachedResponse, found := c.cacheMap[compositeKey]
	if !found {
		return []bson.M{}, false
	}

	// Update last access time
	cachedResponse.lastAccess = c.scheduler.Now()
	return cachedResponse.response, true
}

// Create a new response cache, including starting eviction daemon.
func NewResponseCache(scheduler SchedulerInterface, capacity int) ResponseCache {
	cacheMap := make(map[string]*CacheEntry)
	responseCache := ResponseCache{
		cacheMap:  cacheMap,
		rwLock:    &sync.RWMutex{},
		scheduler: scheduler,
		capacity:  capacity,
	}
	responseCache.startEvictionDaemon()

	return responseCache
}
