import MenuIcon from "@mui/icons-material/Menu";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import IconButton from "@mui/material/IconButton";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Link from "next/link";
import * as React from "react";

const NavBar = () => {
    const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(
        null
    );

    const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElNav(event.currentTarget);
    };

    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };

    return (
        <AppBar position="static" style={{ background: "transparent" }}>
            <Container maxWidth="xl">
                <Toolbar
                    disableGutters
                    className="m-auto max-w-[350px]
                        xs:max-w-[400px] xs:w-full
                        sm:max-w-[620px] xl:flex-row xl:max-w-[1050px] 
                        2xl:max-w-[1100px]"
                >
                    <Link href="/">
                        <span className="inline-flex">
                            <Box
                                component="img"
                                alt="logo"
                                sx={{
                                    display: { xs: "none", md: "flex" },
                                    mr: 0.75,
                                }}
                                src={"/assets/logos/statsugiri_logo_48px.png"}
                            />
                            <Typography
                                variant="h5"
                                noWrap
                                textAlign="center"
                                sx={{
                                    mr: 3,
                                    mt: 1.25,
                                    display: { xs: "none", md: "flex" },
                                    fontWeight: 300,
                                    letterSpacing: ".075rem",
                                    color: "black",
                                }}
                            >
                                Statsugiri
                            </Typography>
                        </span>
                    </Link>

                    <Box
                        sx={{
                            flexGrow: 1,
                            display: { xs: "flex", md: "none" },
                        }}
                    >
                        <IconButton
                            size="large"
                            aria-label="navbar"
                            onClick={handleOpenNavMenu}
                        >
                            <MenuIcon />
                        </IconButton>
                        <Menu
                            id="navbar-items"
                            anchorEl={anchorElNav}
                            anchorOrigin={{
                                vertical: "bottom",
                                horizontal: "left",
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: "top",
                                horizontal: "left",
                            }}
                            open={Boolean(anchorElNav)}
                            onClose={handleCloseNavMenu}
                            sx={{
                                display: { xs: "block", md: "none" },
                            }}
                        >
                            <MenuItem
                                onClick={handleCloseNavMenu}
                                href="/about"
                            >
                                <Typography
                                    textAlign="center"
                                    sx={{ color: "black" }}
                                >
                                    About
                                </Typography>
                            </MenuItem>
                            <MenuItem
                                onClick={handleCloseNavMenu}
                                href="/teams"
                            >
                                <Typography
                                    textAlign="center"
                                    sx={{ color: "black" }}
                                >
                                    PS Teams
                                </Typography>
                            </MenuItem>
                        </Menu>
                    </Box>
                    <Box
                        component="img"
                        alt="logo"
                        sx={{ display: { xs: "flex", md: "none" }, mr: 1 }}
                        src={"/assets/logos/statsugiri_logo_48px.png"}
                    />
                    <Typography
                        variant="h5"
                        noWrap
                        sx={{
                            mr: 2,
                            display: { xs: "flex", md: "none" },
                            flexGrow: 1,
                            fontWeight: 300,
                            letterSpacing: ".075rem",
                            color: "black",
                        }}
                    >
                        Statsugiri
                    </Typography>
                    <Box
                        sx={{
                            ml: 1,
                            flexGrow: 1,
                            display: { xs: "none", md: "flex" },
                        }}
                    >
                        <Button
                            className="block text-zinc-700"
                            onClick={handleCloseNavMenu}
                            sx={{
                                my: 2,
                                ":hover": {
                                    bgcolor: "#e64a75",
                                    color: "white",
                                },
                            }}
                            size="large"
                            href="/about"
                        >
                            About
                        </Button>
                        <Button
                            className="block text-zinc-700"
                            onClick={handleCloseNavMenu}
                            sx={{
                                my: 2,
                                ":hover": {
                                    bgcolor: "#e64a75",
                                    color: "white",
                                },
                            }}
                            size="large"
                            href="/teams"
                        >
                            PS Teams
                        </Button>
                    </Box>
                </Toolbar>
            </Container>
        </AppBar>
    );
};
export default NavBar;
