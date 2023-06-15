import React, { FunctionComponent } from "react";
import { PsTeam } from "@/../types";
import PsTeamItem from "./PsTeamItem";

type Props = {
    teams: readonly PsTeam[];
};

const PsTeamList: FunctionComponent<Props> = ({ teams }) => {
    return (
        <div className="space-y-6">
            {teams.map((team, index) => {
                return (
                    <PsTeamItem
                        key={team.team_id}
                        team={team}
                        rank={index + 1}
                    />
                );
            })}
        </div>
    );
};

export default PsTeamList;
