import Head from "next/head";
import { GetServerSideProps, NextPage } from "next";
import { GetPsTeamsResults } from "../../../types";
import { fetchPsTeams } from "@/api/fetchPsTeams";
import { Format } from "../../../types";
import PsTeamsTableDiv from "@/components/ps_teams/ps_teams_table/PsTeamsTableDiv";
import PsTeamsSearchMenuDiv from "@/components/ps_teams/ps_teams_table_filter/PsTeamsSearchMenuDiv";

const DEFAULT_FORMAT = Format.gen9vgc2023regulationd;

const Teams: NextPage<{ psTeamsResults: GetPsTeamsResults }> = ({
    psTeamsResults,
}) => {
    return (
        <div>
            <Head>
                <title>Statsugiri</title>
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
                    teams={psTeamsResults.teams}
                    snapshotDate={psTeamsResults.snapshot_date.toString()}
                />
            </div>
        </div>
    );
};

export const getServerSideProps: GetServerSideProps = async (context) => {
    // `/teams` provides DEFAULT_FORMAT
    let formatQueryParam: string = context.query.format as string;
    let format =
        formatQueryParam === undefined
            ? "gen9vgc2023regulationd"
            : formatQueryParam;
    console.log("QUERY PARAM:" + formatQueryParam);
    console.log("FORMAT:" + format);
    // const formatQueryParam: string =
    //     context.query.format === undefined
    //         ? DEFAULT_FORMAT
    //         : context.query.format;
    // TODO: Add loading state
    const psTeamsResults = await fetchPsTeams(format);

    return {
        props: {
            psTeamsResults,
        },
    };
};

export default Teams;
