import requests

ROW_OFFSET = 5
NUM_TO_EXTRACT = 40
PKMN_SPLIT_INDEX = 2
STAT_CALC_CONST = 20

# pokdex_req = requests.get("https://play.pokemonshowdown.com/data/pokedex.json")
# pokedex_json = pokdex_req.json()
# print(pokedex_json["bulbasaur"])

# TODO: Docstring
def get_top_usage_pkmn(stats_dump_url: str):
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


def get_pkmn_pokedex_info(pkmn: str):
    return


def calc_max_iv_max_ev_boosting_stat():
    return


def calc_max_iv_max_ev_neutral_stat():
    return


def calc_max_iv_no_ev_neutral_stat():
    return


def calc_min_iv_no_ev_hindering_stat():
    return


def main():
    # TODO: Input for stats URL input
    pkmn_list = get_top_usage_pkmn(
        "https://www.smogon.com/stats/2023-07/gen9vgc2023regulationd-1760.txt"
    )
    print(pkmn_list)
    # TODO: Iterate through Pkmn
    # Get base speed from PS Pokedex


if __name__ == "__main__":
    main()
