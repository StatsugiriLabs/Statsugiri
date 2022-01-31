package utils

// PS! terms
var Formats []string = []string{"gen8vgc2021series11", "gen8ou"}

// DB terms
var DbClusterName string = "babiri-dev-cluster"
var PokemonTeamsSnapshotsCollection string = "pokemon_teams_snapshots"
var PokemonUsageSnapshotsCollection string = "pokemon_usage_snapshots"
var DbEnvPrefix string = Env + "_"
var PokemonTeamSnapshotsCollectionName = DbEnvPrefix + PokemonTeamsSnapshotsCollection
var PokemonUsageSnapshotsCollectionName = DbEnvPrefix + PokemonUsageSnapshotsCollection
