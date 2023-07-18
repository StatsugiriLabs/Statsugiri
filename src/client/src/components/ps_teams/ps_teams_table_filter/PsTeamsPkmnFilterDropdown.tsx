import { useRouter } from "next/router";
import { useState, useEffect, FunctionComponent } from "react";
import FormControl from "@mui/material/FormControl";
import { SelectChangeEvent } from "@mui/material/Select";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import Image from "next/image";
import Autocomplete from "@mui/material/Autocomplete";
import { PsTeam } from "../../../../types";
import { convertToPkmnSpritePath } from "@/utils/pkmnStringUtils";
import { prettifyPkmnName } from "@/utils/pkmnStringUtils";

type Props = {
    teams: PsTeam[];
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

// TODO: Should take in selected Pkmn from query param
const PsTeamsPkmnFilterDropdown: FunctionComponent<Props> = ({ teams }) => {
    const [pkmnSelected, setPkmnSelected] = useState<Array<string>>([]);

    // https://github.com/vercel/next.js/issues/18127#issuecomment-950907739
    const router = useRouter();

    useEffect(() => {
        // Translate state to array string query params
        const pkmnSelectedParam = Array.isArray(pkmnSelected)
            ? pkmnSelected.map((pkmn: string) => pkmn).join(",")
            : "";

        const currPath = router.asPath.split("?")[0];

        if (pkmnSelected.length != 0) {
            router.push({
                pathname: currPath,
                query: { pkmn: pkmnSelectedParam },
            });
        } else {
            router.push({
                pathname: currPath,
            });
        }
    }, [pkmnSelected]);

    const handleChange = (event: SelectChangeEvent) => {
        setPkmnSelected((prevPkmnSelected) => [
            ...(prevPkmnSelected ?? []),
            event.target.value,
        ]);
    };

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
                    options={getPkmnFilterList(teams)}
                    onChange={handleChange}
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
                                src={`/sprites/${convertToPkmnSpritePath(
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
                    onChange={(_, selectedOptions) =>
                        setPkmnSelected(selectedOptions)
                    }
                    className="min-w-[300px] sm:min-w-[560px] md:min-w-[570px] xl:min-w-[340px]"
                />
            </FormControl>
        </div>
    );
};

export default PsTeamsPkmnFilterDropdown;
