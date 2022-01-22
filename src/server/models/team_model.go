package models

// Model for Pokémon Teams
type Team struct {
	PokemonRoster    []string `json:"PokemonRoster,omitempty" validate:"required"`
	Rating           int      `json:"Rating,omitempty" validate:"required"`
	ReplayUploadDate string   `json:"ReplayUploadDate,omitempty" validate:"required"`
}

// Model for Pokémon Team Snapshots
type PokemonTeamsSnapshot struct {
	Date     string `json:"Date,omitempty" validate:"required"`
	FormatId string `json:"FormatId,omitempty" validate:"required"`
	Teams    []Team `json:"Teams,omitempty" validate:"required"`
}
