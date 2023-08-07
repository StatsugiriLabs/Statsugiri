import { fetchPsTeams } from "@/api/fetchPsTeams";
import PsTeamsTableDiv from "@/components/ps_teams/ps_teams_table/PsTeamsTableDiv";
import PsTeamsSearchMenuDiv from "@/components/ps_teams/ps_teams_table_filter/PsTeamsSearchMenuDiv";
import { GetServerSideProps, NextPage } from "next";
import Head from "next/head";
import { Format, GetPsTeamsResults } from "../../../types";

const Teams: NextPage<{
    psTeamsResults: GetPsTeamsResults;
    pkmnToFilter: string[];
}> = ({ psTeamsResults, pkmnToFilter }) => {
    return (
        <div>
            <Head>
                <title>Statsugiri | PS Teams</title>
            </Head>
            <div
                className="flex flex-col m-auto max-w-[350px] space-y-8 mt-6 lg:mt-12
                xs:max-w-[400px] xs:w-full
                sm:max-w-[620px]
                xl:flex-row xl:gap-6 xl:items-start xl:max-w-[1050px] xl:space-y-0
                2xl:max-w-[1100px]"
            >
                <PsTeamsTableDiv psTeamsResults={psTeamsResults} />
                <PsTeamsSearchMenuDiv
                    snapshotDate={psTeamsResults.snapshot_date.toString()}
                    format={psTeamsResults.format_id}
                    teams={psTeamsResults.teams}
                    pkmnToFilter={pkmnToFilter}
                />
            </div>
        </div>
    );
};

export const getServerSideProps: GetServerSideProps = async (context) => {
    // `/teams` provides DEFAULT_FORMAT
    let formatQueryParam: string = context.query.format as string;
    let pkmnQueryParam: string = context.query.pkmn as string;

    const formatToQuery =
        formatQueryParam === undefined
            ? Format.gen9vgc2023regulationd.toString()
            : formatQueryParam;
    const pkmnToFilter =
        pkmnQueryParam === undefined ? [] : pkmnQueryParam.split(",");

    const psTeamsResults = await fetchPsTeams(formatToQuery, pkmnToFilter);

    return {
        props: {
            psTeamsResults,
            pkmnToFilter,
        },
    };
};

export default Teams;
