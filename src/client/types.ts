export interface GetPsTeamsResults {
    num_teams: number;
    format_id: Format;
    snapshot_date: Date;
    teams: PsTeam[];
}

export interface PsTeam {
    team_id: string;
    pkmn_team: string[];
    rating: number;
    replay_id: string;
    replay_upload_date: Date;
}

export enum Format {
    gen9vgc2023regulatione = "gen9vgc2023regulatione",
    gen9vgc2023regulationebo3 = "gen9vgc2023regulationebo3",
    gen9ou = "gen9ou",
}
