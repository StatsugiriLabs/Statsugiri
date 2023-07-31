import { GetPsTeamsResults } from "../../types";
import { BASE_API_URL } from "./constants";

const PS_TEAMS_URL = `${BASE_API_URL}/teams`;

// TODO: Add timeout
export async function fetchPsTeams(
    format: string,
    pkmnToFilter: string[]
): Promise<GetPsTeamsResults> {
    let fetchUrl = `${PS_TEAMS_URL}/${format}/today`;
    // Add filtering parameters if provided (ie. ?pkmn=A&pkmn2=B&pkmn3=C)
    if (pkmnToFilter.length != 0) {
        pkmnToFilter.forEach((pkmn, index) => {
            if (index == 0) {
                fetchUrl += `?pkmn=${pkmn}`;
            } else {
                fetchUrl += `&pkmn${index + 1}=${pkmn}`;
            }
        });
    }
    const response = await fetch(fetchUrl);
    const getPsTeamsResults = await response.json();
    return getPsTeamsResults;
}
