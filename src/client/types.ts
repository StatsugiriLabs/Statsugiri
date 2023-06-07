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
    Gen9Vgc2023RegulationC = "gen9vgc2023regulationc",
    Gen9Ou = "gen9ou",
}
