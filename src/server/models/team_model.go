package models

// Model for Pokémon Teams
type Team struct {
	PokemonRoster    []string
	Rating           int32
	ReplayUploadDate string
}

// Model for Pokémon Team Snapshots
type PokemonTeamsSnapshot struct {
	Date     string
	FormatId string
	Teams    []Team
}
