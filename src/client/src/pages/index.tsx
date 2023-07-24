import Head from "next/head";
import { GetStaticProps, NextPage } from "next";

const Home: NextPage = () => {
    return (
        <div>
            <Head>
                <title>Statsugiri</title>
            </Head>
            <p>Howdy, this index is temporary</p>
        </div>
    );
};

export default Home;
