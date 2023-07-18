import Head from "next/head";
import { GetStaticProps, NextPage } from "next";
import { Format, GetPsTeamsResults } from "../../types";
import { fetchPsTeams } from "@/api/fetchPsTeams";
import PsTeamTable from "@/components/ps_teams/ps_teams_table/PsTeamsTable";
import PsTeamSearchBar from "@/components/ps_teams/ps_teams_table_filter/PsTeamsFormatDropdown";

const Home: NextPage<{ psTeamsResults: GetPsTeamsResults }> = ({
    psTeamsResults,
}) => {
    return (
        <div>
            <Head>
                <title>Statsugiri</title>
            </Head>
            <p>Howdy, this index is temporary</p>
            <PsTeamSearchBar />
            <PsTeamTable teams={psTeamsResults.teams} />
        </div>
    );
};

export const getStaticProps: GetStaticProps = async () => {
    const psTeamsResults = await fetchPsTeams(
        Format.gen9vgc2023regulationd.toString()
    );

    return {
        props: {
            psTeamsResults,
        },
    };
};

export default Home;
