package cache

import (
	"sync"
	"time"

	"go.mongodb.org/mongo-driver/bson"
)

const (
	TTL         = 30   // Cache entry lifetime from last access (seconds)
	MAX_ENTRIES = 1000 // Maximum number of entries in cache
)

type CacheEntry struct {
	response   []bson.M
	lastAccess int64
}

type ResponseCache struct {
	// Let key be compositeKey
	cacheMap map[string]*CacheEntry
	rwLock   *sync.RWMutex
}

// Start daemon for evicting expired cache entries.
func (c *ResponseCache) startEvictionDaemon() {
	go func() {
		for now := range time.Tick(time.Second) {
			c.rwLock.Lock()
			for compositeKey, item := range c.cacheMap {
				// Remove expired entries
				if now.Unix()-item.lastAccess > int64(TTL) {
					c.evictCacheEntry(compositeKey)
				}
			}
			c.rwLock.Unlock()
		}
	}()
}

// Evict cache entry.
func (c *ResponseCache) evictCacheEntry(compositeKey string) {
	_, exists := c.cacheMap[compositeKey]

	if exists {
		delete(c.cacheMap, compositeKey)
	}
}

// Check if cache is full denoted by MAX_ENTRIES.
func (c *ResponseCache) IsCacheFull() bool {
	c.rwLock.Lock()
	defer c.rwLock.Unlock()

	if len(c.cacheMap) >= MAX_ENTRIES {
		return true
	}
	return false
}

func (c *ResponseCache) Put(compositeKey string, response []bson.M) {
	c.rwLock.Lock()
	defer c.rwLock.Unlock()

	_, found := c.cacheMap[compositeKey]
	if !found {
		cacheEntry := &CacheEntry{
			response:   response,
			lastAccess: time.Now().Unix(),
		}
		c.cacheMap[compositeKey] = cacheEntry
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
	cachedResponse.lastAccess = time.Now().Unix()
	return cachedResponse.response, true
}

// Create a new response cache, including starting eviction daemon.
func NewResponseCache() ResponseCache {
	cacheMap := make(map[string]*CacheEntry)
	responseCache := ResponseCache{
		cacheMap: cacheMap,
		rwLock:   &sync.RWMutex{},
	}
	responseCache.startEvictionDaemon()

	return responseCache
}
