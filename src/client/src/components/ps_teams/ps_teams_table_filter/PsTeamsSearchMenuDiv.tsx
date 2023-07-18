import { FunctionComponent } from "react";
import PsTeamsSearchMenu from "./PsTeamsSearchMenu";
import { PsTeam } from "../../../../types";

type Props = {
    teams: PsTeam[];
    snapshotDate: string;
};

const PsTeamsSearchMenuDiv: FunctionComponent<Props> = ({
    teams,
    snapshotDate,
}) => {
    return (
        <div className="w-full">
            <h2 className="text-3xl font-medium mb-5">Filters</h2>
            <PsTeamsSearchMenu teams={teams} snapshotDate={snapshotDate} />
        </div>
    );
};

export default PsTeamsSearchMenuDiv;
