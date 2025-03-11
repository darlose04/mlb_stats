# game stats here
# make separate file for playoff games
import statsapi
import json
from dotenv import load_dotenv
import mysql.connector
import os
from datetime import datetime, timedelta
import sys

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

add_games_to_db = (
    "INSERT INTO games "
    "(id, game_guid, feed_link, game_type, season, game_date, official_date, away_team, away_team_id, away_team_score, away_team_total_wins, away_team_total_losses, away_team_series_number, home_team, home_team_id, home_team_score, home_team_total_wins, home_team_total_losses, home_team_series_number, number_of_games_in_series, series_game_number, venue_name, venue_id) "
    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
)

# probably just going to grab the entire year
# then filter the results for regular season games

# years = [2025]
# year =
# while year < 2025:
#     years.append(year)
#     year += 1

# checking number of games that don't get added
games_not_added = 0

# TODO: Will need to get the current date to use for the startDate and endDate
# will need to run the script every night - maybe get the previous day of data and run the script early in the morning

current_date = datetime.now()
previous_day = current_date - timedelta(days=1)
previous_day_string = previous_day.strftime("%m/%d/%Y")
print(previous_day_string)

# for year in years:
schedule = statsapi.get(
    "schedule",
    {
        "sportId": 1,
        "startDate": f"{previous_day_string}",
        "endDate": f"{previous_day_string}",
    },
)

# print("Schedule Keys", schedule.keys())
# print("Total Games", schedule["totalGames"])

schedule_dates = schedule["dates"]
# print(json.dumps(schedule_dates, indent=4))

total_games = []

for date in schedule_dates:
    games = date["games"]

    filtered_games = list(filter(lambda game: game["gameType"] == "S", games))

    # print(filtered_games)
    check_duplicate = 0
    for game in filtered_games:
        if game["status"]["detailedState"] == "Final":

            # print("================")
            # print(json.dumps(game, indent=4))
            # print("================")
            if "resumeDate" in game:
                print("resume date in game, continuuing")
                continue
            elif "score" not in game["teams"]["away"]:
                games_not_added += 1
                print(json.dumps(game, indent=4))
                continue
            else:
                game_date = datetime.strptime(game["gameDate"], "%Y-%m-%dT%H:%M:%SZ")
                official_date = datetime.strptime(game["officialDate"], "%Y-%m-%d")

                game_insert = (
                    game["gamePk"],
                    game["gameGuid"],
                    game["link"],
                    game["gameType"],
                    game["season"],
                    game_date,
                    official_date,
                    game["teams"]["away"]["team"]["name"],
                    game["teams"]["away"]["team"]["id"],
                    game["teams"]["away"]["score"],
                    game["teams"]["away"]["leagueRecord"]["wins"],
                    game["teams"]["away"]["leagueRecord"]["losses"],
                    game["teams"]["away"]["seriesNumber"],
                    game["teams"]["home"]["team"]["name"],
                    game["teams"]["home"]["team"]["id"],
                    game["teams"]["home"]["score"],
                    game["teams"]["home"]["leagueRecord"]["wins"],
                    game["teams"]["home"]["leagueRecord"]["losses"],
                    game["teams"]["home"]["seriesNumber"],
                    game["gamesInSeries"],
                    game["seriesGameNumber"],
                    game["venue"]["name"],
                    game["venue"]["id"],
                )

                total_games.append(game_insert)

try:
    cursor.executemany(add_games_to_db, total_games)
    cnx.commit()
except mysql.connector.Error as err:
    print(f"ERROR: {err}")
    cnx.rollback()
finally:
    print("done with year insert")

cursor.close()
cnx.close()
print("Games not added: ", games_not_added)
