import {
    convertToPkmnSpritePath,
    prettifyPkmnName,
} from "@/utils/pkmnStringUtils";
import Paper from "@mui/material/Paper";
import Router from "next/router";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import Tooltip from "@mui/material/Tooltip";
import Image from "next/image";
import { FunctionComponent, useState } from "react";
import { PsTeam } from "../../../../types";

type Props = {
    teams: readonly PsTeam[];
};

const REPLAY_BASE_URL = "https://replay.pokemonshowdown.com/";
const DEFAULT_TEAMS_PER_PAGE = 10;
const DEFAULT_PAGE_INDEX = 0;

const PKMN_SPRITE_SIZE = 55;
const REPLAY_SPRITE_SIZE = 30;
// TODO: Move vs-recorder sprite path
const REPLAY_SPRITE_PATH = "/vs-recorder.png";
const PAPER_ELEVATION = 2;

interface PsTeamsTableColumn {
    id: "rating" | "pkmn_team" | "replay_upload_date" | "replay_id";
    label: string;
    minWidth?: number;
    align?: "left" | "right" | "center";
}

const columns: PsTeamsTableColumn[] = [
    { id: "rating", label: "Rating", align: "center" },
    { id: "pkmn_team", label: "Team", align: "left" },
    { id: "replay_upload_date", label: "Uploaded", align: "center" },
    { id: "replay_id", label: "Replay" },
];

const renderCell = (team: PsTeam, column: PsTeamsTableColumn) => {
    const cellValue = team[column.id];
    switch (column.id) {
        case "pkmn_team":
            return (
                <TableCell
                    key={column.id}
                    align={column.align}
                    className="grid gap-x-1 sm:grid-cols-2 md:grid-cols-6"
                >
                    {team.pkmn_team.map((pkmn) => (
                        <Tooltip
                            title={
                                <p
                                    style={{
                                        fontWeight: "bold",
                                    }}
                                >
                                    {prettifyPkmnName(pkmn)}
                                </p>
                            }
                            key={pkmn}
                            placement="top"
                            arrow
                        >
                            {/* TODO: Attempt global state to push to pkmnSelected */}
                            <Image
                                key={pkmn}
                                src={`/sprites/${convertToPkmnSpritePath(
                                    pkmn
                                )}.png`}
                                width={PKMN_SPRITE_SIZE}
                                height={PKMN_SPRITE_SIZE}
                                alt={pkmn}
                                onClick={() => {
                                    const currPath =
                                        Router.asPath.split("?")[0];
                                    Router.push({
                                        pathname: currPath,
                                        query: {
                                            pkmn: prettifyPkmnName(pkmn),
                                        },
                                    });
                                }}
                            />
                        </Tooltip>
                    ))}
                </TableCell>
            );
        case "replay_id":
            return (
                <TableCell key={column.id}>
                    {/* Image alignment requires wrapper: https://github.com/vercel/next.js/discussions/18375 */}
                    <div className="flex justify-center replay-id-icon">
                        <a
                            target="_blank"
                            href={`${REPLAY_BASE_URL}${team.replay_id}`}
                        >
                            <Image
                                key={team.replay_id}
                                src={REPLAY_SPRITE_PATH}
                                width={REPLAY_SPRITE_SIZE}
                                height={REPLAY_SPRITE_SIZE}
                                alt={team.replay_id}
                            />
                        </a>
                    </div>
                </TableCell>
            );
        default:
            return (
                <TableCell
                    key={column.id}
                    align={column.align}
                    className="text-sm text-zinc-700"
                >
                    {cellValue.toString()}
                </TableCell>
            );
    }
};

const PsTeamsTable: FunctionComponent<Props> = ({ teams }) => {
    const [page, setPage] = useState(DEFAULT_PAGE_INDEX);
    const [rowsPerPage, setRowsPerPage] = useState(DEFAULT_TEAMS_PER_PAGE);

    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (
        event: React.ChangeEvent<HTMLInputElement>
    ) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };
    return (
        <Paper elevation={PAPER_ELEVATION}>
            <TableContainer className="h-auto w-full flex-1 max-h-[800px]">
                <Table size="small" aria-label="PS Teams Service Table">
                    <TableHead>
                        <TableRow>
                            {columns.map((column) => (
                                <TableCell
                                    key={column.id}
                                    align={column.align}
                                    className="py-4"
                                >
                                    <b>{column.label.toUpperCase()}</b>
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {teams
                            .slice(
                                page * rowsPerPage,
                                page * rowsPerPage + rowsPerPage
                            )
                            .map((team) => {
                                return (
                                    <TableRow
                                        hover
                                        tabIndex={-1}
                                        key={team.team_id}
                                    >
                                        {columns.map((column) => {
                                            return renderCell(team, column);
                                        })}
                                    </TableRow>
                                );
                            })}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                rowsPerPageOptions={[10, 25, 50, 100]}
                component="div"
                count={teams.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
        </Paper>
    );
};

export default PsTeamsTable;
