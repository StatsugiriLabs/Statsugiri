package responses

// Response for `teams` endpoint.
type TeamsResponse struct {
	NumResults            int
	Page                  int
	Limit                 int
	PokemonTeamsSnapshots []PokemonTeamsSnapshot
}

// Response-level equivalent to `models.team_model`
type Team struct {
	PokemonRoster    []string
	Rating           int32
	ReplayUploadDate string
}

type PokemonTeamsSnapshot struct {
	Date     string
	FormatId string
	Teams    []Team
}
