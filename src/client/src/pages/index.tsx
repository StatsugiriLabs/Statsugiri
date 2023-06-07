import Head from "next/head";
import { GetStaticProps, NextPage } from "next";
import { GetPsTeamsResults, PsTeam } from "../../types";
import PsTeamList from "../components/PsTeamList";
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
    const psTeamsResults = await fetchPsTeams("gen9vgc2023regulationc");

    return {
        props: {
            psTeamsResults,
        },
    };
};

export default Home;
