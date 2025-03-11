import json
import uuid


def player_fielding(game_id, data):
    insert_format = (
        "INSERT INTO player_fielding "
        "(id,player_id,game_id,name,link,position_name,position_type,team_id,fielding_caught_stealing,fielding_sb,assists,putouts,errors,chances,fielding,fielding_passed_ball,fielding_pickoffs) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )

    players = []

    away_player_ids = data["teams"]["away"]["players"].keys()
    home_player_ids = data["teams"]["home"]["players"].keys()
    away_team_id = data["teams"]["away"]["team"]["id"]
    home_team_id = data["teams"]["home"]["team"]["id"]

    for player_id in away_player_ids:
        player = data["teams"]["away"]["players"][player_id]

        if player["stats"]["fielding"]:
            stats = player["stats"]["fielding"]
            fielding = float(stats["fielding"])

            fielding_insert = (
                str(game_id) + "_" + str(player["person"]["id"]),
                player["person"]["id"],
                game_id,
                player["person"]["fullName"],
                player["person"]["link"],
                player["position"]["name"],
                player["position"]["type"],
                away_team_id,
                stats["caughtStealing"],
                stats["stolenBases"],
                stats["assists"],
                stats["putOuts"],
                stats["errors"],
                stats["chances"],
                fielding,
                stats["passedBall"],
                stats["pickoffs"],
            )

            players.append(fielding_insert)

    for player_id in home_player_ids:
        player = data["teams"]["home"]["players"][player_id]

        if player["stats"]["fielding"]:
            stats = player["stats"]["fielding"]
            fielding = float(stats["fielding"])

            fielding_insert = (
                str(game_id) + "_" + str(player["person"]["id"]),
                player["person"]["id"],
                game_id,
                player["person"]["fullName"],
                player["person"]["link"],
                player["position"]["name"],
                player["position"]["type"],
                home_team_id,
                stats["caughtStealing"],
                stats["stolenBases"],
                stats["assists"],
                stats["putOuts"],
                stats["errors"],
                stats["chances"],
                fielding,
                stats["passedBall"],
                stats["pickoffs"],
            )

            players.append(fielding_insert)

    return {"insert_format": insert_format, "boxscore_insert": players}
