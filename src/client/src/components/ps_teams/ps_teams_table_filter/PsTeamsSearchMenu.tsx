import { FunctionComponent } from "react";
import { Box } from "@mui/material";
import Paper from "@mui/material/Paper";
import PsTeamsDateDropdown from "./PsTeamsDateDropdown";
import PsTeamsFormatDropdown from "./PsTeamsFormatDropdown";
import PsTeamsPkmnFilterDropdown from "./PsTeamsPkmnFilterDropdown";
import PsTeamsFilterResetButton from "./PsTeamsFilterResetButton";
import { PsTeam } from "../../../../types";

const PAPER_ELEVATION = 2;

type Props = {
    teams: PsTeam[];
    snapshotDate: string;
};

const PsTeamsSearchMenu: FunctionComponent<Props> = ({
    teams,
    snapshotDate,
}) => {
    return (
        <Paper elevation={PAPER_ELEVATION}>
            <Box className="flex flex-col rounded-lg p-7 gap-3.5 w-full xl:min-w-[320px]">
                <PsTeamsDateDropdown snapshotDate={snapshotDate} />
                <PsTeamsFormatDropdown />
                {/* <PsTeamsPkmnFilterDropdown teams={teams} /> */}
                <PsTeamsFilterResetButton />
            </Box>
        </Paper>
    );
};

export default PsTeamsSearchMenu;
