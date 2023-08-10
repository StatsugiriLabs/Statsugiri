import Layout from "@/components/shared/Layout";
import Loading from "@/components/shared/Loading";
import "@/styles/globals.css";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import type { AppProps } from "next/app";
import Router from "next/router";
import { useEffect, useState } from "react";

const theme = createTheme({
    typography: {
        fontFamily: [
            "-apple-system",
            "BlinkMacSystemFont",
            '"Segoe UI"',
            "Roboto",
            '"Helvetica Neue"',
            "Arial",
            "sans-serif",
            '"Apple Color Emoji"',
            '"Segoe UI Emoji"',
            '"Segoe UI Symbol"',
        ].join(","),
    },
});

export default function App({ Component, pageProps }: AppProps) {
    // https://stackoverflow.com/questions/60755316/next-js-getserversideprops-show-loading/60756105#60756105
    const [loading, setLoading] = useState(false);
    useEffect(() => {
        const start = () => {
            setLoading(true);
        };
        const end = () => {
            setLoading(false);
        };
        Router.events.on("routeChangeStart", start);
        Router.events.on("routeChangeComplete", end);
        Router.events.on("routeChangeError", end);
        return () => {
            Router.events.off("routeChangeStart", start);
            Router.events.off("routeChangeComplete", end);
            Router.events.off("routeChangeError", end);
        };
    }, []);
    return (
        <ThemeProvider theme={theme}>
            <Layout>
                {loading ? <Loading /> : <Component {...pageProps} />}
            </Layout>
        </ThemeProvider>
    );
}
