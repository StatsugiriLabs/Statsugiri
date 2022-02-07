package responses

type UsageResponse struct {
	NumResults     int
	Page           int
	Limit          int
	UsageSnapshots []UsageSnapshot
}

type UsageSnapshot struct {
	Date          string
	FormatId      string
	PokemonUsages []PokemonUsage
}

type PokemonUsage struct {
	Pokemon string
	Usage   int
}

type RatingUsageResponse struct {
	NumResults           int
	Page                 int
	Limit                int
	RatingUsageSnapshots []RatingUsageSnapshot
}

type RatingUsageSnapshot struct {
	Date                       string
	FormatId                   string
	PokemonAverageRatingUsages []PokemonAverageRatingUsage
}

type PokemonAverageRatingUsage struct {
	Pokemon            string
	AverageRatingUsage int
}

type PartnerUsageResponse struct {
	NumResults            int
	Page                  int
	Limit                 int
	PartnerUsageSnapshots []PartnerUsageSnapshot
}

type PartnerUsageSnapshot struct {
	Date                 string
	FormatId             string
	PokemonPartnerUsages []PokemonPartnerUsage
}

type PokemonPartnerUsage struct {
	Pokemon       string
	PartnerUsages []PartnerUsage
}

type PartnerUsage struct {
	Partner string
	Usage   int
}
