import json
import logging
import time
from enum import Enum
from typing import List

import requests

POKEDEX_SRC = "https://play.pokemonshowdown.com/data/pokedex.json"

ROW_OFFSET = 5
NUM_TO_EXTRACT = 50
PKMN_SPLIT_INDEX = 2
OUTPUT_DIR = "output"

STAT_CONST = 5
MAX_EVS = 252
MIN_EVS = 0
MAX_IVS = 31
MIN_IVS = 0
BOOSTING_MULT = 1.1
NEUTRAL_MULT = 1
HINDERING_MULT = 0.9

BASE_SPEED_LABEL = "base_speed"
MAX_IV_MAX_EV_BOOSTING_STAT_LABEL = "max_iv_max_ev_boosting_stat"
MAX_IV_MAX_EV_NEUTRAL_STAT_LABEL = "max_iv_max_ev_neutral_stat"
MAX_IV_NO_EV_NEUTRAL_STAT_LABEL = "max_iv_no_ev_neutral_stat"
MIN_IV_NO_EV_HINDERING_STAT = "min_iv_no_ev_hindering_stat"


class NatureType(Enum):
    HINDERING = 1
    NEUTRAL = 2
    BOOSTING = 3


NATURE_MULT_MAP = {
    NatureType.HINDERING: HINDERING_MULT,
    NatureType.NEUTRAL: NEUTRAL_MULT,
    NatureType.BOOSTING: BOOSTING_MULT,
}

# Initialize logger
logger = logging.getLogger()
logging.basicConfig(format="%(message)s")
logger.setLevel(logging.INFO)

# Convert Pkmn names to Pokedex JSON format
def sanitize_pkmn(pkmn: str) -> str:
    ARTIFACTS = ["-", " "]
    for artifact in ARTIFACTS:
        pkmn = pkmn.replace(artifact, "")
    return pkmn.lower()


def get_stats_dump_tag(url: str) -> str:
    stats_dump_suffix = url.split("stats/")[1]
    stats_dump_tag = stats_dump_suffix.split(".")[0]
    return stats_dump_tag.replace("/", "_")


# Get top usage Pkmn given stats dump URL
def get_top_usage_pkmn(stats_dump_url: str) -> List[str]:
    try:
        # Fetch usage table records
        chaos_usage_req = requests.get(stats_dump_url)
        chaos_usage_text = chaos_usage_req.text
        chaos_usage_rows = chaos_usage_text.split("\n")[ROW_OFFSET:]

        pkmn_list = []
        for row in chaos_usage_rows[:NUM_TO_EXTRACT]:
            # Split record into columns
            col_data = row.split("|")
            pkmn_list.append(col_data[PKMN_SPLIT_INDEX].strip())
        return pkmn_list
    except Exception as e:
        logger.error("🔴 Error retrieving Pokémon usage, {e}".format(e=str(e)))
        return []


# Get Pokedex object
def get_pkmn_pokedex_json() -> dict:
    try:
        pokdex_req = requests.get(POKEDEX_SRC)
        pokedex_json = pokdex_req.json()
        return pokedex_json
    except Exception as e:
        logger.error("🔴 Error retrieving Pokedex, {e}".format(e=str(e)))
        return {}


# Calc modified stat from base stat, IV, EV, and nature type
def calc_numerical_stat(
    base_spd_stat: int, iv_investment: int, ev_investment: int, nature_type: NatureType
):
    # Base stat + 5 + (IV/2 + EVs/8) followed by nature multiplier
    # IV, EV, and nature multiplier are truncated via integer
    nature_mult = NATURE_MULT_MAP[nature_type]
    return int(
        (
            base_spd_stat
            + STAT_CONST
            + int(iv_investment / 2)
            + int(ev_investment / 8)
            + (ev_investment % 8 != 0)
        )
        * nature_mult
    )


def calc_max_iv_max_ev_boosting_stat(base_spd_stat: int):
    return calc_numerical_stat(base_spd_stat, MAX_IVS, MAX_EVS, NatureType.BOOSTING)


def calc_max_iv_max_ev_neutral_stat(base_spd_stat: int):
    return calc_numerical_stat(base_spd_stat, MAX_IVS, MAX_EVS, NatureType.NEUTRAL)


def calc_max_iv_no_ev_neutral_stat(base_spd_stat: int):
    return calc_numerical_stat(base_spd_stat, MAX_IVS, MIN_EVS, NatureType.NEUTRAL)


def calc_min_iv_no_ev_hindering_stat(base_spd_stat: int):
    return calc_numerical_stat(base_spd_stat, MIN_IVS, MIN_EVS, NatureType.HINDERING)


def main():
    pkmn_spds_dict = {}

    pokedex_json = get_pkmn_pokedex_json()
    if not pokedex_json:
        logger.error("🔴 Cannot retrieve Pokedex object, aborting...")
        return

    stats_dump_src = input(
        "🔵 Please provide the stats dump URL (ie. `https://www.smogon.com/stats/2023-07/gen9vgc2023regulationd-1760.txt`).\n"
    )
    stats_dump_tag = get_stats_dump_tag(stats_dump_src)

    pkmn_list = get_top_usage_pkmn(stats_dump_src)
    if not pkmn_list:
        logger.error("🔴 Cannot retrieve Pokedex object, aborting...")
        return

    confirmation = input(
        "🔵 Preparing speed tier export for '{stats_dump_src}'. Press 'Y' to proceed with export.\n".format(
            stats_dump_src=stats_dump_src
        )
    ).strip()
    if confirmation != "Y":
        logger.info("🔵 No confirmation provided. Export script is aborting.")
        exit()

    logger.info(
        "Initializing speed tier export for '{stats_dump_src}'.".format(
            stats_dump_src=stats_dump_src
        )
    )
    start_time = time.time()
    for pkmn in pkmn_list:
        pkmn_base_spd = pokedex_json[sanitize_pkmn(pkmn)]["baseStats"]["spe"]
        pkmn_spds_dict[pkmn] = {
            BASE_SPEED_LABEL: pkmn_base_spd,
            MAX_IV_MAX_EV_BOOSTING_STAT_LABEL: calc_max_iv_max_ev_boosting_stat(
                pkmn_base_spd
            ),
            MAX_IV_MAX_EV_NEUTRAL_STAT_LABEL: calc_max_iv_max_ev_neutral_stat(
                pkmn_base_spd
            ),
            MAX_IV_NO_EV_NEUTRAL_STAT_LABEL: calc_max_iv_no_ev_neutral_stat(
                pkmn_base_spd
            ),
            MIN_IV_NO_EV_HINDERING_STAT: calc_min_iv_no_ev_hindering_stat(
                pkmn_base_spd
            ),
        }

    output_path = "{output_dir}/{tag}.json".format(
        output_dir=OUTPUT_DIR, tag=stats_dump_tag
    )
    with open(output_path, "w") as fp:
        json.dump(pkmn_spds_dict, fp)

    logger.info(
        "🔵 Speed tier export processed in {time} seconds. Exported to '{output_path}'.".format(
            time=str(time.time() - start_time), output_path=output_path
        )
    )


if __name__ == "__main__":
    main()
