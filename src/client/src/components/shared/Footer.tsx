import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import { Favorite, Twitter, GitHub } from "@mui/icons-material";

const Footer = () => {
    return (
        <Box className="w-full h-auto py-12 gap-y-5">
            <Container maxWidth="lg">
                <Grid container direction="column" alignItems="center">
                    <Grid item xs={12}>
                        <Typography className="text-sm text-zinc-500">
                            <a
                                href="https://ko-fi.com/statsugiri"
                                target="_blank"
                            >
                                <Favorite sx={{ fontSize: 15 }} /> Support Us
                            </a>{" "}
                            |{" "}
                            <a
                                href="https://twitter.com/Statsugiri"
                                target="_blank"
                            >
                                <Twitter sx={{ fontSize: 15 }} /> Follow Us
                            </a>{" "}
                            |{" "}
                            <a
                                href="https://github.com/StatsugiriLabs/Statsugiri"
                                target="_blank"
                            >
                                <GitHub sx={{ fontSize: 15 }} /> Build with Us
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
