import { FunctionComponent } from "react";
import { PsTeam } from "../../types";
import Image from "next/image";
import { getPkmnSpriteName } from "@/utils/getPkmnSpriteName";

type Props = {
    rank: number;
    team: PsTeam;
};

const PsTeamItem: FunctionComponent<Props> = ({ rank, team }) => {
    return (
        <div>
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
