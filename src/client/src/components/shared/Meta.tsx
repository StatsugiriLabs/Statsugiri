import Head from "next/head";
import { FunctionComponent } from "react";

interface Props {
    title?: string;
    keywords?: string;
    description?: string;
}

const defaultProps: Props = {
    title: "Statsugiri",
    keywords: "pokemon, vgc, stats, gaming, pokemonshowdown",
    description: "A competitive Pokémon data platform",
};

const Meta: FunctionComponent<Props> = ({ title, keywords, description }) => {
    return (
        <Head>
            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            />
            <meta name="keywords" content={keywords} />
            <meta name="description" content={description} />
            <meta charSet="utf-8" />
            <link rel="icon" href="/favicon.ico" />
            <title>{title}</title>
        </Head>
    );
};

Meta.defaultProps = defaultProps;

export default Meta;
