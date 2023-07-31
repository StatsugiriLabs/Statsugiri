import {
    convertToPkmnSpritePath,
    prettifyPkmnName,
} from "@/utils/pkmnStringUtils";
import Autocomplete from "@mui/material/Autocomplete";
import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import TextField from "@mui/material/TextField";
import Image from "next/image";
import Router from "next/router";
import { FunctionComponent, useEffect, useRef, useState } from "react";
import { PsTeam } from "../../../../types";

type Props = {
    teams: PsTeam[];
    pkmnToFilter: string[];
};

const PKMN_FILTER_SPRITE_SIZE = 40;

export function getPkmnFilterList(teams: PsTeam[]): string[] {
    const pkmnList = teams.map((team) => team.pkmn_team).flat();
    // Filter for unique items
    const pkmnSet = pkmnList.filter(
        (pkmn, index) => pkmnList.indexOf(pkmn) === index
    );
    // Clean up set items
    let pkmnFilterSet: string[] = [];
    pkmnSet.forEach((pkmn) => {
        pkmnFilterSet.push(prettifyPkmnName(pkmn));
    });
    return pkmnFilterSet.sort();
}

const PsTeamsPkmnFilterDropdown: FunctionComponent<Props> = ({
    teams,
    pkmnToFilter,
}) => {
    const [pkmnSelected, setPkmnSelected] = useState<Array<string>>(
        pkmnToFilter === undefined ? [] : pkmnToFilter
    );
    const firstUpdate = useRef(true);

    useEffect(() => {
        if (firstUpdate.current) {
            firstUpdate.current = false;
            return;
        }
        // Translate state to array string query params
        const pkmnSelectedParam = Array.isArray(pkmnSelected)
            ? pkmnSelected.map((pkmn: string) => pkmn).join(",")
            : "";
        const currPath = Router.asPath.split("?")[0];

        if (pkmnSelected.length != 0) {
            Router.push({
                pathname: currPath,
                query: {
                    pkmn: pkmnSelectedParam,
                },
            });
        } else {
            Router.push({
                pathname: currPath,
            });
        }
    }, [pkmnSelected]);

    return (
        <div>
            <FormControl size="small">
                {/* Value provided to Autocomplete is invalid is a known issue: 
                https://github.com/mui/material-ui/issues/29727 */}
                <label className="font-light text-sm mb-1 text-zinc-700">
                    Filter by Pokémon
                </label>
                <Autocomplete
                    id="ps-teams-pkmn-filter-dropdown-label"
                    value={pkmnSelected}
                    multiple
                    disableCloseOnSelect
                    disablePortal
                    isOptionEqualToValue={(option, pkmmSelected) =>
                        option.valueOf() == pkmmSelected.valueOf()
                    }
                    onChange={(_, selectedOptions) =>
                        setPkmnSelected(selectedOptions)
                    }
                    options={getPkmnFilterList(teams)}
                    renderOption={(props, pkmn) => (
                        <Box
                            component="li"
                            sx={{ "& > img": { mr: 1, flexShrink: 0 } }}
                            {...props}
                        >
                            <Image
                                loading="lazy"
                                width={PKMN_FILTER_SPRITE_SIZE}
                                height={PKMN_FILTER_SPRITE_SIZE}
                                src={`/assets/pkmn_sprites/${convertToPkmnSpritePath(
                                    pkmn
                                )}.png`}
                                alt={pkmn}
                            />
                            <div className="text-base text-zinc-700">
                                {pkmn}
                            </div>
                        </Box>
                    )}
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            label="Pokémon..."
                            inputProps={{
                                ...params.inputProps,
                            }}
                        />
                    )}
                    className="min-w-[300px] sm:min-w-[560px] md:min-w-[570px] xl:min-w-[340px]"
                />
            </FormControl>
        </div>
    );
};

export default PsTeamsPkmnFilterDropdown;
