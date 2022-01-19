package responses


// Response for getting most recent recorded teams for specific format
type TeamResponse struct {
	Status int		`json:"status"`
	Message string	`json:"message"`
	Data map[string]interface{}		`json:"data"`
}
