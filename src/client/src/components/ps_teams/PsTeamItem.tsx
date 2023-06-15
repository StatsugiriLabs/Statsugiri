import { FunctionComponent } from "react";
import { PsTeam } from "../../../types";
import Image from "next/image";
import { getPkmnSpriteName } from "@/utils/getPkmnSpriteName";

const SPRITE_SIZE = 90;
const REPLAY_BASE_URL = "https://replay.pokemonshowdown.com/";

type Props = {
    rank: number;
    team: PsTeam;
};

const PsTeamItem: FunctionComponent<Props> = ({ rank, team }) => {
    return (
        <div className="rounded border-2 border-gray-250 shadow-md">
            <div className="flow-root py-2 bg-slate-200">
                <h3 className="float-left ml-3">{`#${rank}`}</h3>
                <h4 className="float-right mr-3">{`Rating: ${team.rating}`}</h4>
            </div>
            <div className="mt-3 mx-5">
                {team.pkmn_team.map((pkmn, index) => {
                    return (
                        <Image
                            key={index}
                            src={`/../public/sprites/${getPkmnSpriteName(
                                pkmn
                            )}.png`}
                            width={SPRITE_SIZE}
                            height={SPRITE_SIZE}
                            alt={pkmn}
                            style={{ display: "inline" }}
                        />
                    );
                })}
                <div className="mt-2">
                    <p>
                        <i>Uploaded: {`${team.replay_upload_date}`}</i>
                    </p>
                    <button className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center mb-4">
                        <a
                            href={REPLAY_BASE_URL + "/" + team.replay_id}
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Replay 🔗
                        </a>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default PsTeamItem;
