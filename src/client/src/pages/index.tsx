import Head from "next/head";
import { GetStaticProps, NextPage } from "next";
import { GetPsTeamsResults } from "../../types";
import PsTeamList from "@/components/ps_teams/PsTeamList";
import { fetchPsTeams } from "@/api/fetchPsTeams";

const Home: NextPage<{ psTeamsResults: GetPsTeamsResults }> = ({
    psTeamsResults,
}) => {
    return (
        <div>
            <Head>
                <title>Statsugiri</title>
            </Head>
            <PsTeamList teams={psTeamsResults.teams} />
        </div>
    );
};

export const getStaticProps: GetStaticProps = async (context) => {
    const psTeamsResults = await fetchPsTeams("gen9vgc2023regulationd");

    return {
        props: {
            psTeamsResults,
        },
    };
};

export default Home;
