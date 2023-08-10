import Box from "@mui/material/Box";

const Loading = () => {
    return (
        <div className="grid grid-cols-9 pt-12">
            <Box
                component="img"
                alt="loading"
                src={"/assets/loading/tatsugiri.gif"}
            />
            <Box
                component="img"
                alt="loading"
                src={"/assets/loading/tatsugiri-stretchy.gif"}
            />
            <Box
                component="img"
                alt="loading"
                src={"/assets/loading/tatsugiri-droopy.gif"}
            />
        </div>
    );
};

export default Loading;
