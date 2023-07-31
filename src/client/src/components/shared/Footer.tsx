import { Favorite, GitHub, Twitter } from "@mui/icons-material";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";

const Footer = () => {
    return (
        <Box className="w-full h-auto py-12 gap-y-5">
            <Container maxWidth="lg">
                <Grid container direction="column" alignItems="center">
                    <Grid item xs={12}>
                        <Typography className="text-sm text-zinc-500">
                            <Favorite sx={{ fontSize: 15 }} />
                            <a
                                href="https://ko-fi.com/statsugiri"
                                target="_blank"
                                className="mx-1 text-blue-500 hover:text-blue-800"
                            >
                                Support Us
                            </a>{" "}
                            | <Twitter sx={{ fontSize: 15 }} />
                            <a
                                href="https://twitter.com/Statsugiri"
                                target="_blank"
                                className="mx-1 text-blue-500 hover:text-blue-800"
                            >
                                Follow Us
                            </a>{" "}
                            | <GitHub sx={{ fontSize: 15 }} />
                            <a
                                href="https://github.com/StatsugiriLabs/Statsugiri"
                                target="_blank"
                                className="mx-1 text-blue-500 hover:text-blue-800"
                            >
                                Build with Us
                            </a>
                        </Typography>
                    </Grid>
                </Grid>
                <Box className="mt-1">
                    <Typography className="text-sm text-center text-zinc-500">
                        Pokémon and All Respective Names are Trademark & © of
                        Nintendo 1996-{new Date().getFullYear()}
                    </Typography>
                </Box>
            </Container>
        </Box>
    );
};

export default Footer;
