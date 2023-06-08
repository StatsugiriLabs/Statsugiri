import { FunctionComponent } from "react";
import { PsTeam } from "../../../types";
import Image from "next/image";
import { getPkmnSpriteName } from "@/utils/getPkmnSpriteName";

type Props = {
    rank: number;
    team: PsTeam;
};

const PsTeamItem: FunctionComponent<Props> = ({ rank, team }) => {
    return (
        <div>
            <a
                href="#"
                className="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
            >
                <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                    Noteworthy technology acquisitions 2021
                </h5>
                <p className="font-normal text-gray-700 dark:text-gray-400">
                    Here are the biggest enterprise technology acquisitions of
                    2021 so far, in reverse chronological order.
                </p>
            </a>
            <p>{"Rank #" + rank}</p>
            {team.pkmn_team.map((pkmn, index) => {
                return (
                    <Image
                        key={index}
                        src={`/../public/sprites/${getPkmnSpriteName(
                            pkmn
                        )}.png`}
                        width={75}
                        height={75}
                        alt={pkmn}
                        style={{ display: "inline" }}
                    />
                );
            })}
            <p>{"Rating: " + team.rating}</p>
            <p>{"Replay ID: " + team.replay_id}</p>
            <hr />
        </div>
    );
};

export default PsTeamItem;
