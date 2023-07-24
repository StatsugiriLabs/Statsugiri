import { Box } from "@mui/material";
import Paper from "@mui/material/Paper";
import { FunctionComponent } from "react";
import { PsTeam } from "../../../../types";
import PsTeamsDateDropdown from "./PsTeamsDateDropdown";
import PsTeamsFormatDropdown from "./PsTeamsFormatDropdown";
import PsTeamsPkmnFilterDropdown from "./PsTeamsPkmnFilterDropdown";

const PAPER_ELEVATION = 2;

type Props = {
    snapshotDate: string;
    format: string;
    teams: PsTeam[];
    pkmnToFilter: string[];
};

const PsTeamsSearchMenu: FunctionComponent<Props> = ({
    snapshotDate,
    format,
    teams,
    pkmnToFilter,
}) => {
    return (
        <Paper elevation={PAPER_ELEVATION}>
            <Box className="flex flex-col rounded-lg p-7 gap-3.5 w-full xl:min-w-[320px]">
                <PsTeamsDateDropdown snapshotDate={snapshotDate} />
                <PsTeamsFormatDropdown format={format} />
                <PsTeamsPkmnFilterDropdown
                    teams={teams}
                    pkmnToFilter={pkmnToFilter}
                />
            </Box>
        </Paper>
    );
};

export default PsTeamsSearchMenu;
