import statsapi
import json
import requests
from dotenv import load_dotenv
import mysql.connector
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
# from game_1 import game_one
# from game_2 import game_two
# from game_3 import game_three

# TODO: at some point will need to use the player link to get the bat and throw side of hitters and pitchers

load_dotenv()

db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWD"),
    "port": os.getenv("DB_PORT"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB"),
}
cnx = mysql.connector.connect(**db_config)
print("connected to db")
cursor = cnx.cursor()

get_existing_ids = "select distinct game_id from mlb.team_boxscores_home_batting"

cursor.execute(
    get_existing_ids,
)

exist_ids = []

for id in cursor:
    exist_ids.append(id[0])

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
sys.exit()
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
        cursor.execute(htbs_insert, home_team_batting_stats)
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error in home team batting: {err}")
        cnx.rollback()

    try:
        cursor.execute(atbs_insert, away_team_batting_stats)
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error away team batting: {err}")
        cnx.rollback()

    try:
        cursor.execute(atpfs_insert, away_team_p_and_f_stats)
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error in away team pitching/fielding: {err}")
        cnx.rollback()

    try:
        cursor.execute(htpfs_insert, home_team_p_and_f_stats)
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error in home team pitching/fielding: {err}")
        cnx.rollback()

    try:
        cursor.executemany(pb_insert, pb_stats)
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error in player batting: {err}")
        cnx.rollback()

    try:
        cursor.executemany(pp_insert, pp_stats)
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error in player pitching: {err}")
        cnx.rollback()

    try:
        cursor.executemany(pf_insert, pf_stats)
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error in player fielding: {err}")
        cnx.rollback()
    finally:
        print("adding stats to db")

cursor.close()
cnx.close()
