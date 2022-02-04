package responses

type TimeSeriesUsageResponse struct {
	Pokemon string
	FormatUsageSnapshots []FormatUsageSnapshot
}

type FormatUsageSnapshot struct {
	FormatId string
	TimeSeriesUsageSnapshots []TimeSeriesUsageSnapshot	
}

type TimeSeriesUsageSnapshot struct {
	Date string
	Usage int
}
