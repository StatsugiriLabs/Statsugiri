import { GetPsTeamsResults } from "../../types";
import { BASE_API_URL } from "./constants";

const PS_TEAMS_URL = `${BASE_API_URL}/teams`;

// TODO: Offer options for filtering
// TODO: Add timeout
export async function fetchPsTeams(format: string): Promise<GetPsTeamsResults> {
    const response = await fetch(`${PS_TEAMS_URL}/${format}/today`);
    const getPsTeamsResults = await response.json();
    return getPsTeamsResults;
}
