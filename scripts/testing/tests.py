import requests
import datetime
import statsapi
import json
from scripts.testing.boxscore_data import boxscore_dict

# TODO: Need to figure out what to get for database tables
# create separate files for each table that needs to be created
# Teams, games, players (pitchers, hitters), playoff games

# Could create functions, import them, and then pass in command line arguments
# so there's no need to run every function

# "fields": "dates,date,games,gamePk"
# schedule = statsapi.get(
#     "schedule",
#     {
#         "sportId": 1,
#         "startDate": "03/20/2024",
#         "endDate": "09/30/2024",
#         "team": "New York Yankees",
#     },
# )
# schedule = statsapi.schedule(start_date="3/28/2014", end_date="9/30/2014", sportId=1)

year = 2014
schedule = statsapi.get(
    "schedule",
    {"sportId": 1, "startDate": f"01/01/{year}", "endDate": f"12/31/{year}"},
)
# print(json.dumps(schedule, indent=4))
# print("Schedule Keys", schedule.keys())

# print(len(schedule))
# num_games = []
for day in schedule["dates"]:
    games = day["games"]
    for game in games:
        if game["gamePk"] == 380538:
            print(json.dumps(game, indent=4))

""" 
each date is an item in the returned array. the games will nested down in the arrays and objects
 """
# print("Total Games", schedule["totalGames"])

# boxscore = boxscore_dict()
# response = requests.get("https://statsapi.mlb.com/api/v1/game/746820/boxscore")
# boxscore = response.json()

# players = boxscore["teams"]["away"]["players"]
# boxscore = statsapi.boxscore_data(746820)

# print(json.dumps(boxscore["teams"]["away"]["players"], indent=4))

# print(boxscore.keys())
# print(players.keys())

# print(schedule['dates'])


# schedule_dates = schedule["dates"]
# print(json.dumps(schedule_dates[0], indent=4))

# for date in schedule_dates:
#     games = date["games"]

#     # returns regular season games
#     new_list = list(filter(lambda game: game["gameType"] == "R", games))

#     print(json.dumps(new_list, indent=4))

# for game in games:
#     print(game)
#     print("---------------------------------------")


# pretty_json = json.dumps(schedule_dates, indent=4)
# print(pretty_json)
print("=========================")
# boxscore formatted text
# print(statsapi.boxscore(746175))
# boxscore data
# print(json.dumps(statsapi.boxscore_data(746175), indent=4))
