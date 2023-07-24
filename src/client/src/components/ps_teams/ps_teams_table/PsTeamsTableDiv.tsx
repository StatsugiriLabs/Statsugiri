import PsTeamTable from "@/components/ps_teams/ps_teams_table/PsTeamsTable";
import { NextPage } from "next";
import { GetPsTeamsResults } from "../../../../types";

const PsTeamsTableDiv: NextPage<{ psTeamsResults: GetPsTeamsResults }> = ({
    psTeamsResults,
}) => {
    return (
        <div className="flex-1 w-full xl:sticky xl:top-4 xl:min-w-[640px] 2xl:min-w-[720px]">
            <h2 className="text-3xl font-medium mb-4">Best Teams</h2>
            <PsTeamTable teams={psTeamsResults.teams} />
        </div>
    );
};

export default PsTeamsTableDiv;
