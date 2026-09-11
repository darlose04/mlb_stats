# game stats here
# make separate file for playoff games
import statsapi
import json
from dotenv import load_dotenv
import psycopg2
import os
from datetime import datetime, timedelta
import sys
from db import get_connection, dual_write

load_dotenv()

cnx = get_connection()
print("connected to db")
cursor = cnx.cursor()

add_games_to_db = (
    "INSERT INTO games "
    "(id, game_guid, feed_link, game_type, season, game_date, official_date, away_team, away_team_id, away_team_score, away_team_total_wins, away_team_total_losses, away_team_series_number, home_team, home_team_id, home_team_score, home_team_total_wins, home_team_total_losses, home_team_series_number, number_of_games_in_series, series_game_number, venue_name, venue_id) "
    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    "ON CONFLICT (id) DO NOTHING"
)

add_games_to_scheduled = (
    "INSERT INTO scheduled_games "
    "(id, game_guid, feed_link, game_type, season, game_date, official_date, away_team, away_team_id,away_team_total_wins, away_team_total_losses, away_team_series_number, home_team, home_team_id, home_team_total_wins, home_team_total_losses, home_team_series_number, number_of_games_in_series, series_game_number, venue_name, venue_id, home_probable_pitcher, away_probable_pitcher) "
    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    "ON CONFLICT (id) DO NOTHING"
)

# probably just going to grab the entire year
# then filter the results for regular season games

# years = [2026]
year = 2026
# while year < 2010:
#     years.append(year)
#     year += 1

# checking number of games that don't get added
games_not_added = 0
# games skipped because they already exist in the games table
games_already_exist = 0

# grab every game id already in the db so we can skip duplicates
# (lets the script be rerun over a full season without hitting games_pkey)
cursor.execute("SELECT id FROM games")
existing_game_ids = {row[0] for row in cursor.fetchall()}
print("Existing games in db: ", len(existing_game_ids))

# TODO: Will need to get the current date to use for the startDate and endDate
# will need to run the script every night - maybe get the previous day of data and run the script early in the morning

current_date = datetime.now()
previous_day = current_date - timedelta(days=1)
previous_day_string = previous_day.strftime("%m/%d/%Y")
print("Previous Day: ", previous_day_string)

# for year in years:
schedule = statsapi.get(
    "schedule",
    {
        "sportId": 1,
        # "startDate": f"{previous_day_string}",
        # "endDate": f"{previous_day_string}",
        "startDate": f"03/01/{year}",
        "endDate": f"10/10/{year}",
    },
)

# print("Schedule: ", json.dumps(schedule, indent=4))
# print("Schedule Keys", schedule.keys())
# print("Total Games", schedule["totalGames"])

schedule_dates = schedule["dates"]
# print(json.dumps(schedule_dates, indent=4))

total_games = []
scheduled_games = []

for date in schedule_dates:
    games = date["games"]

    filtered_games = list(filter(lambda game: game["gameType"] == "R", games))

    # print(filtered_games)
    check_duplicate = 0
    for game in filtered_games:
        if game["status"]["detailedState"] == "Final":

            # print("================")
            # print(json.dumps(game, indent=4))
            # print("================")
            if game["gamePk"] in existing_game_ids:
                games_already_exist += 1
                continue
            elif "resumeDate" in game:
                print("resume date in game, continuing")
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
        elif game["status"]["detailedState"] == "Scheduled":
            # print("scheduled games: ", json.dumps(game, indent=4))
            scheduled_data = statsapi.schedule(game_id=game["gamePk"])
            # print("probables: ", json.dumps(scheduled_data, indent=4))
            home_probable_pitcher = (
                scheduled_data[0]["home_probable_pitcher"]
                if (scheduled_data[0]["home_probable_pitcher"] != "")
                else None
            )
            away_probable_pitcher = (
                scheduled_data[0]["away_probable_pitcher"]
                if (scheduled_data[0]["away_probable_pitcher"] != "")
                else None
            )
            game_date = datetime.strptime(game["gameDate"], "%Y-%m-%dT%H:%M:%SZ")
            official_date = datetime.strptime(game["officialDate"], "%Y-%m-%d")
            schedule_insert = (
                game["gamePk"],
                game["gameGuid"],
                game["link"],
                game["gameType"],
                game["season"],
                game_date,
                official_date,
                game["teams"]["away"]["team"]["name"],
                game["teams"]["away"]["team"]["id"],
                game["teams"]["away"]["leagueRecord"]["wins"],
                game["teams"]["away"]["leagueRecord"]["losses"],
                game["teams"]["away"]["seriesNumber"],
                game["teams"]["home"]["team"]["name"],
                game["teams"]["home"]["team"]["id"],
                game["teams"]["home"]["leagueRecord"]["wins"],
                game["teams"]["home"]["leagueRecord"]["losses"],
                game["teams"]["home"]["seriesNumber"],
                game["gamesInSeries"],
                game["seriesGameNumber"],
                game["venue"]["name"],
                game["venue"]["id"],
                home_probable_pitcher,
                away_probable_pitcher,
            )

            scheduled_games.append(schedule_insert)

if total_games:
    try:
        dual_write(cnx, add_games_to_db, total_games, many=True)
    except psycopg2.Error:
        pass  # dual_write already prints the error
    finally:
        print("done with year insert")
else:
    print("no new games to insert")

cursor.execute("TRUNCATE TABLE scheduled_games, fantasy.scheduled_games")
cnx.commit()
if scheduled_games:
    try:
        dual_write(cnx, add_games_to_scheduled, scheduled_games, many=True)
    except psycopg2.Error:
        pass  # dual_write already prints the error
    finally:
        print("done with year insert")
else:
    print("no new games to insert")


cursor.close()
cnx.close()
print("Games inserted: ", len(total_games))
print("Games skipped (already in db): ", games_already_exist)
print("Games not added: ", games_not_added)
