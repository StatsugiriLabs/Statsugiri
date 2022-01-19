package models

type Team struct {
	Pokemon_Roster []string
	Rating int
	Replay_Upload_Date string
}

type PokemonTeamsSnapshot struct {
	Date string				`json:"date,omitempty" validate:"required"`
	Format_ID string		`json:"format,omitempty" validate:"required"`
	Teams []Team			`json:"team,omitempty" validate:"required"`
}
