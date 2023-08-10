import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";

const Home: NextPage = () => {
    return (
        <div>
            <Head>
                <title>Statsugiri | Competitive Pokémon Data Platform</title>
            </Head>
            <div
                className="flex flex-col m-auto max-w-[350px] space-y-8 mt-6 lg:mt-12
                xs:max-w-[400px] xs:w-full
                sm:max-w-[620px]
                xl:flex-row xl:gap-6 xl:items-start xl:max-w-[1050px] xl:space-y-0
                2xl:max-w-[1100px]"
            >
                <div className="pb-20">
                    <h2 className="text-6xl font-normal pb-5">
                        Power your Pokémon data insights
                    </h2>
                    <h4 className="text-xl font-light pb-1">
                        Statsugiri is a competitive Pokémon data platform. Take
                        command of your tourney and metagame analysis.
                    </h4>
                    <Link href="/teams">
                        <Button
                            variant="outlined"
                            size="large"
                            sx={{
                                my: 2,
                                ":hover": {
                                    bgcolor: "#247dd5",
                                    color: "white",
                                },
                            }}
                        >
                            Get Started
                        </Button>
                    </Link>
                </div>
                <Box
                    className="max-w-0  xl:max-w-[630px] mr-1"
                    component="img"
                    alt="logo"
                    src={"/assets/branding/pkmn_stat_flat.png"}
                />
            </div>
            <div
                className="flex flex-col p-2 sm:mx-12 md:mx-0 md:p-0 max-w-[350px] xs:max-w-[400px] sm:max-w-[620px] 
                xl:max-w-[1050px] xl:m-auto 2xl:max-w-[1100px]"
            >
                <h2 className="text-4xl pb-6">Meet our tools</h2>
                <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
                    <Link
                        href="/teams"
                        className="flex flex-col p-6 py-4 rounded-lg gap-2 border-2"
                    >
                        <p className="text-lg font-normal">PS Teams</p>
                        <p className="text-sm font-light leading-relaxed font-body mb-3">
                            Find the best public teams and replays from Pokémon
                            Showdown. Filter through teams by specific Pokémon
                            combinations. New teams are updated automatically
                            every day.
                        </p>
                    </Link>
                    <a
                        href="https://twitter.com/Statsugiri"
                        target="_blank"
                        className="flex flex-col p-6 py-4 rounded-lg gap-2 border-2"
                    >
                        <p className="text-lg font-normal">More coming soon</p>
                        <p className="text-sm font-light leading-relaxed font-body mb-3">
                            Keep an eye on our Twitter @Statsugiri for new
                            updates!
                        </p>
                    </a>
                </div>
            </div>
        </div>
    );
};

export default Home;
