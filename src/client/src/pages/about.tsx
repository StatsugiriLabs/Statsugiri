import Head from "next/head";
const About = () => {
    return (
        <div
            className="m-auto max-w-[350px] mt-6 lg:mt-12
        xs:max-w-[400px] xs:w-full
        sm:max-w-[620px]
        xl:flex-row xl:gap-6 xl:items-start xl:max-w-[1050px] xl:space-y-0
        2xl:max-w-[1100px] text-base text-zinc-700"
        >
            <Head>
                <title>Statsugiri | About</title>
            </Head>
            <h2 className="text-4xl font-medium pb-4">About</h2>
            <p>
                Statsugiri is a competitive Pokémon data platform focused on the{" "}
                <a
                    href="https://www.pokemon.com/us/play-pokemon/pokemon-events/pokemon-tournaments/video-game/"
                    target="_blank"
                    className="text-blue-500 hover:text-blue-800"
                >
                    Pokémon Video Game Championship (VGC) Series
                </a>
                . Our goal is to provide players with tools for teambuilding and
                analysis to make informed decisions in their tournament
                preparation.
            </p>
            <br />
            <p>
                Initially known as{" "}
                <a
                    href="https://github.com/kelvinkoon/babiri_v1/tree/master"
                    target="_blank"
                    className="text-blue-500 hover:text-blue-800"
                >
                    babiri.net
                </a>
                , we are excited to continue building data-driven VGC tools as
                the game grows. We have taken heavy inspiration from similar
                sites such as{" "}
                <a
                    href="https://pikalytics.com/"
                    target="_blank"
                    className="text-blue-500 hover:text-blue-800"
                >
                    Pikalytics
                </a>{" "}
                and{" "}
                <a
                    href="https://github.com/bul-ikana/vgcstats"
                    target="_blank"
                    className="text-blue-500 hover:text-blue-800"
                >
                    VGC Stats
                </a>
                , who have made massive contributions to the field. A special
                thanks to{" "}
                <a
                    href="https://play.pokemonshowdown.com/sprites/gen5/"
                    target="_blank"
                    className="text-blue-500 hover:text-blue-800"
                >
                    Pokémon Showdown
                </a>{" "}
                for providing the sprites and data to make the project possible.
            </p>
            <br />
            <p>
                Statsugiri is an ads-free, open-source project. If you are
                interested in contributing or learning more, please visit our{" "}
                <a
                    href="https://github.com/StatsugiriLabs/Statsugiri"
                    target="_blank"
                    className="text-blue-500 hover:text-blue-800"
                >
                    Github
                </a>{" "}
                or{" "}
                <a
                    href="https://kelvinkoon.dev/tags/statsugiri/"
                    target="_blank"
                    className="text-blue-500 hover:text-blue-800"
                >
                    engineering blog
                </a>{" "}
                for more details.
            </p>
            <h2 className="text-4xl font-medium pt-8 pb-4">FAQ</h2>
            <div className="mb-4">
                <h4 className="text-xl font-medium mb-2">
                    What technologies power Statsugiri?
                </h4>
                <p>
                    Statsugiri is powered primarily by AWS. The data pipeline
                    runs on Step Functions, Lambda, and S3. The back-end is
                    hosted on Lambda and API Gateway. The front-end uses Next.js
                    hosted on DigitalOcean&apos;s App Platform. The
                    infrastructure is provisioned via Cloud Development Kit
                    (CDK) with CI/CD hosted on Github Actions. Detailed
                    write-ups are available on our engineering blog.
                </p>
            </div>
            <div className="my-4">
                <h4 className="text-xl font-medium my-2">
                    How does the PS Teams service work?
                </h4>
                <p>
                    Every day, the public replays from top-performing users on{" "}
                    <a
                        href="https://pokemonshowdown.com/"
                        target="_blank"
                        className="text-blue-500 hover:text-blue-800"
                    >
                        Pokémon Showdown
                    </a>{" "}
                    are retrieved. The replays are sorted by the user&apos;s
                    rating on the ladder. If a user does not have any replays
                    for the format, the next user is retrieved until 100 replays
                    are recorded. Bots are not used to retrieve replays, as only
                    public replays are aggregated.
                </p>
            </div>
            <div className="my-4">
                <h4 className="text-xl font-medium my-2">
                    How can I support Statsugiri?
                </h4>
                <p>
                    If you enjoy Statsugiri, please consider supporting our{" "}
                    <a
                        href="https://ko-fi.com/statsugiri#"
                        target="_blank"
                        className="text-blue-500 hover:text-blue-800"
                    >
                        Ko-fi
                    </a>{" "}
                    or{" "}
                    <a
                        href="https://ko-fi.com/statsugiri#"
                        target="_blank"
                        className="text-blue-500 hover:text-blue-800"
                    >
                        Github Sponsors
                    </a>
                    . Your support enables our team to work on new features and
                    take care of operational costs.
                </p>
            </div>
            <div className="my-4">
                <h4 className="text-xl font-medium my-2">
                    Why is it called Statsugiri?
                </h4>
                <p>
                    Statsugiri is a portmanteau of statistics and{" "}
                    <a
                        href="https://bulbapedia.bulbagarden.net/wiki/Tatsugiri_(Pok%C3%A9mon)"
                        target="_blank"
                        className="text-blue-500 hover:text-blue-800"
                    >
                        Tatsugiri
                    </a>
                    , the False Dragon Titan introduced in the Paldea region.
                    The logo is a silhouette of Tatsugiri&apos;s tail.
                </p>
            </div>
            <div className="my-4">
                <h4 className="text-xl font-medium my-2">
                    Does Statsugiri collect user information?
                </h4>
                <p>
                    Statsugiri does not run ads to provide a clean user
                    experience. We also do not use cookies to collect user
                    information as Google Analytics would. Instead, we leverage
                    privacy-first web analytics from{" "}
                    <a
                        href="https://blog.cloudflare.com/privacy-first-web-analytics/"
                        target="_blank"
                        className="text-blue-500 hover:text-blue-800"
                    >
                        CloudFlare
                    </a>{" "}
                    as a security-conscious alternative.
                </p>
            </div>
            <h2 className="text-4xl font-medium pt-8 pb-4">Contact Us</h2>
            <p>
                We are active on Twitter{" "}
                <a
                    href="https://twitter.com/Statsugiri"
                    target="_blank"
                    className="text-blue-500 hover:text-blue-800"
                >
                    @Statsugiri
                </a>
                . We can also be reached by email via &apos;
                <i>&lt;website&gt;@gmail.com</i>&apos;. Feel free to use either
                for feature requests or bug reports.
            </p>
        </div>
    );
};

export default About;
