import statsapi
import json
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB"),
}
cnx = mysql.connector.connect(**db_config)
print("connected to db")
cursor = cnx.cursor()

add_teams_to_db = (
    "INSERT INTO teams "
    "(id, name, venue_id, venue_name, league_id, league_name) "
    "VALUES (%s, %s, %s, %s, %s, %s)"
)

# May need to add other teams from older seasons like the Expos or teams that have changed names
# the ids didn't though, so trying to add a new team with an existing id primary key will throw an error

# season = 1998
# while season < 2024:
#     season += 1


# teams_get = statsapi.get("teams", {"sportId": 1, "season": season})
teams_get = statsapi.get("teams", {"sportId": 1})
teams = teams_get["teams"]

# print(json.dumps(teams, indent=4))
team_data = []

for team in teams:
    # team_id = team["id"]
    # team_name = team["name"]
    # venue_id = team["venue"]["id"]
    # venue_name = team["venue"]["name"]
    # league_id = team["league"]["id"]
    # league_name = team["league"]["name"]

    team_insert = (
        team["id"],
        team["name"],
        team["venue"]["id"],
        team["venue"]["name"],
        team["league"]["id"],
        team["league"]["name"],
    )

    team_data.append(team_insert)

try:
    cursor.executemany(add_teams_to_db, team_data)
    cnx.commit()
    print(f"Inserted {cursor.rowcount} row(s) with ID: {cursor.lastrowid}")

except mysql.connector.Error as err:
    print(f"ERROR: {err}")
    cnx.rollback()

finally:
    cursor.close()
    cnx.close()
