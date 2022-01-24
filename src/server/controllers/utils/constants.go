package utils

// PS! terms
var Formats []string = []string{"gen8vgc2021series11", "gen8ou"}

// DB terms
var DbEnvPrefix string = Env + "_"
var PokemonTeamSnapshotsCollectionName = DbEnvPrefix + PokemonTeamsSnapshotsCollection
var PokemonUsageSnapshotsCollectionName = DbEnvPrefix + PokemonUsageSnapshotsCollection
