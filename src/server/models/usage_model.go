package models

// Model for Pokémon Usage
type PokemonUsage struct {
	Usage           int      `json:"Rating,omitempty" validate:"required"`
}

// Model for Pokémon Partner Usage
type PokemonPartnerUsage struct {
	PartnerUsage           map[string]int 
}

// Model for Pokémon Usage Snapshots
type PokemonUsageSnapshot struct {
	Date     string `json:"Date,omitempty" validate:"required"`
	FormatId string `json:"FormatId,omitempty" validate:"required"`
	PokemonUsage    map[string]int 
	PokemonPartnerUsage map[string]map[string]int
	PokemonAverageRatingUsage map[string]int
}