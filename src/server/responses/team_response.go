package responses

// Response for `teams` endpoint.
type TeamsResponse struct {
	Page                  int
	Limit                 int
	PokemonTeamsSnapshots []PokemonTeamSnapshot
}

type PokemonTeamSnapshot struct {
	Date             string
	FormatId         string
	PokemonRoster    []string
	Rating           int
	ReplayUploadDate string
}
