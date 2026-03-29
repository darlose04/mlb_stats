import statsapi
import json
import requests
from dotenv import load_dotenv
import psycopg2
import os
import sys
from datetime import datetime
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

# TODO: can probably get the current year without setting it manually. Not really necessary at this point though.
game_ids = get_ids(cursor, 2025)
print(game_ids)

difference = list(set(game_ids) - set(exist_ids))
# print(difference)

# sys.exit(0)
# game_id = 745039
# boxscore = boxscore_dict()
# print(json.dumps(boxscore, indent=4))

# game_ids = [745039, 745037, 745035]
# game_boxscore = game_three()
# sys.exit()
for game_id in difference:
    # for game_id in game_ids:
    response = requests.get(f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore")
    game_boxscore = response.json()

    pp_info = player_pitching(game_id, game_boxscore)

    pp_insert = pp_info["insert_format"]
    pp_stats = pp_info["boxscore_insert"]

    pb_info = player_batting(game_id, game_boxscore)

    pb_insert = pb_info["insert_format"]
    pb_stats = pb_info["boxscore_insert"]

    pf_info = player_fielding(game_id, game_boxscore)

    pf_insert = pf_info["insert_format"]
    pf_stats = pf_info["boxscore_insert"]

    away_team_batting_stats = []
    atbs_response = away_team_batting(game_id, game_boxscore)
    atbs_insert = atbs_response["insert_format"]
    away_team_batting_stats = atbs_response["boxscore_insert"]

    home_team_batting_stats = []
    htbs_response = home_team_batting(game_id, game_boxscore)
    htbs_insert = htbs_response["insert_format"]
    home_team_batting_stats = htbs_response["boxscore_insert"]

    away_team_p_and_f_stats = []
    atpfs_response = away_team_pitching_and_fielding(game_id, game_boxscore)
    atpfs_insert = atpfs_response["insert_format"]
    away_team_p_and_f_stats = atpfs_response["boxscore_insert"]

    home_team_p_and_f_stats = []
    htpfs_response = home_team_pitching_and_fielding(game_id, game_boxscore)
    htpfs_insert = htpfs_response["insert_format"]
    home_team_p_and_f_stats = htpfs_response["boxscore_insert"]

    print("adding game id: ", game_id)
    # Note: need to account for player duplication since each player is using a unique id
    # maybe create a custom unique id and check for that
    # like game_id + player_id
    try:
        dual_write(cnx, htbs_insert, home_team_batting_stats)
        print("Committed home team batting")

        dual_write(cnx, atbs_insert, away_team_batting_stats)
        print("Committed away team batting")

        dual_write(cnx, atpfs_insert, away_team_p_and_f_stats)
        print("Committed away team pitching/fielding")

        dual_write(cnx, htpfs_insert, home_team_p_and_f_stats)
        print("Committed home team pitching/fielding")

        dual_write(cnx, pb_insert, pb_stats, many=True)
        print("Committed player batting")

        dual_write(cnx, pp_insert, pp_stats, many=True)
        print("Committed player pitching")

        dual_write(cnx, pf_insert, pf_stats, many=True)
        print("Committed player fielding")
    except psycopg2.Error:
        print(f"Error processing game {game_id}, skipping remaining inserts for this game")
    finally:
        print("adding stats to db")

cursor.close()
cnx.close()
