package cache

import "time"

// SchedulerInterface manages scheduling for go routines.
type SchedulerInterface interface {
	CreateTicker(d time.Duration) <-chan time.Time
	Now() int64
}

type Scheduler struct{}

// Creates a channel to deliver ticks at provided interval.
func (s *Scheduler) CreateTicker(d time.Duration) <-chan time.Time {
	ticker := time.NewTicker(d)
	return ticker.C
}

// Returns the current Unix timestamp.
func (s *Scheduler) Now() int64 {
	now := time.Now().Unix()
	return now
}
