import { FunctionComponent } from "react";
import { PsTeam } from "../../../../types";
import PsTeamsSearchMenu from "./PsTeamsSearchMenu";

type Props = {
    snapshotDate: string;
    format: string;
    teams: PsTeam[];
    pkmnToFilter: string[];
};

const PsTeamsSearchMenuDiv: FunctionComponent<Props> = ({
    format,
    teams,
    pkmnToFilter,
}) => {
    return (
        <div className="w-full">
            <h2 className="text-3xl font-medium mb-4">Filters</h2>
            <PsTeamsSearchMenu
                teams={teams}
                format={format}
                pkmnToFilter={pkmnToFilter}
            />
        </div>
    );
};

export default PsTeamsSearchMenuDiv;
