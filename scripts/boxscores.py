import statsapi
import json
import requests
from dotenv import load_dotenv
import psycopg2
import os
import sys
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# from scripts.testing.boxscore_data import boxscore_dict
from tools import get_ids
from boxscores_away_batting import away_team_batting
from boxscores_home_batting import home_team_batting
from boxscores_away_p_and_f import away_team_pitching_and_fielding
from boxscores_home_p_and_f import home_team_pitching_and_fielding
from player_batting import player_batting
from player_pitching import player_pitching
from player_fielding import player_fielding
from db import get_connection, dual_write

# from game_1 import game_one
# from game_2 import game_two
# from game_3 import game_three

# TODO: at some point will need to use the player link to get the bat and throw side of hitters and pitchers

load_dotenv()

cnx = get_connection()
print("connected to db")
cursor = cnx.cursor()

get_existing_ids = "select distinct game_id from team_boxscores_home_batting"

cursor.execute(
    get_existing_ids,
)


exist_ids = []

for id in cursor:
    exist_ids.append(id[0])

MAX_WORKERS = 15


def fetch_and_transform(game_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(
                f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"
            )
            response.raise_for_status()
            game_boxscore = response.json()

            return {
                "game_id": game_id,
                "pp": player_pitching(game_id, game_boxscore),
                "pb": player_batting(game_id, game_boxscore),
                "pf": player_fielding(game_id, game_boxscore),
                "atbs": away_team_batting(game_id, game_boxscore),
                "htbs": home_team_batting(game_id, game_boxscore),
                "atpfs": away_team_pitching_and_fielding(game_id, game_boxscore),
                "htpfs": home_team_pitching_and_fielding(game_id, game_boxscore),
            }
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2**attempt)
            else:
                raise


for season in range(2026, 2027):
    game_ids = get_ids(cursor, season)
    difference = list(set(game_ids) - set(exist_ids))

    if not difference:
        print(f"Season {season}: no new games to process, skipping")
        continue

    print(
        f"Season {season}: fetching boxscores for {len(difference)} games with {MAX_WORKERS} threads..."
    )
    results = []
    errors = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_game = {
            executor.submit(fetch_and_transform, gid): gid for gid in difference
        }

        for future in as_completed(future_to_game):
            game_id = future_to_game[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error fetching game {game_id}: {e}")
                errors.append(game_id)

    print(f"Season {season}: fetched {len(results)} games, {len(errors)} errors")

    for result in results:
        game_id = result["game_id"]
        print("adding game id: ", game_id)
        try:
            dual_write(
                cnx, result["htbs"]["insert_format"], result["htbs"]["boxscore_insert"]
            )
            dual_write(
                cnx, result["atbs"]["insert_format"], result["atbs"]["boxscore_insert"]
            )
            dual_write(
                cnx,
                result["atpfs"]["insert_format"],
                result["atpfs"]["boxscore_insert"],
            )
            dual_write(
                cnx,
                result["htpfs"]["insert_format"],
                result["htpfs"]["boxscore_insert"],
            )
            dual_write(
                cnx,
                result["pb"]["insert_format"],
                result["pb"]["boxscore_insert"],
                many=True,
            )
            dual_write(
                cnx,
                result["pp"]["insert_format"],
                result["pp"]["boxscore_insert"],
                many=True,
            )
            dual_write(
                cnx,
                result["pf"]["insert_format"],
                result["pf"]["boxscore_insert"],
                many=True,
            )
        except psycopg2.Error:
            print(
                f"Error processing game {game_id}, skipping remaining inserts for this game"
            )

    if errors:
        print(f"Season {season}: failed to fetch {len(errors)} games: {errors}")

cursor.close()
cnx.close()
