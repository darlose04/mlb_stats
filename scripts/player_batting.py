import json
import uuid

# just need to use the stats key
# need to get the batting stats for home and away players
# will need to account for NL pitchers before the DH was placed in the NL


def player_batting(game_id, data):
    # print(json.dumps(data, indent=4))
    insert_format = (
        "INSERT INTO player_batting "
        "(id,player_id,game_id,name,link,position_name,position_type,team_id,batting_order,flyouts,groundouts,airouts,runs,rbi,singles,doubles,triples,homeruns,strikeouts,walks,intentional_walks,hits,hbp,at_bats,plate_appearances,avg,obp,slg,ops,caught_stealing,stolen_bases,gidp,gitp,total_bases,lob,sac_bunts,sac_flies,catchers_int,pickoffs,popouts,lineouts ) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )

    batters = []

    away_player_ids = data["teams"]["away"]["players"].keys()
    home_player_ids = data["teams"]["home"]["players"].keys()
    away_team_id = data["teams"]["away"]["team"]["id"]
    home_team_id = data["teams"]["home"]["team"]["id"]

    # print(away_batter_ids)
    # print(home_batter_ids)

    for player_id in away_player_ids:
        player = data["teams"]["away"]["players"][player_id]

        if player["stats"]["batting"]:
            stats = player["stats"]["batting"]
            avg = stats["hits"] / stats["atBats"] if stats["atBats"] != 0 else None
            obp_numerator = stats["hits"] + stats["baseOnBalls"] + stats["hitByPitch"]
            obp_denominator = (
                stats["atBats"]
                + stats["baseOnBalls"]
                + stats["hitByPitch"]
                + stats["sacFlies"]
            )
            obp = obp_numerator / obp_denominator if obp_denominator != 0 else None
            slg = (
                stats["totalBases"] / stats["atBats"] if stats["atBats"] != 0 else None
            )
            ops = obp + slg if slg != None else obp
            singles = stats["hits"] - (
                stats["doubles"] + stats["triples"] + stats["homeRuns"]
            )

            batter_insert = (
                str(game_id) + "_" + str(player["person"]["id"]),
                player["person"]["id"],
                game_id,
                player["person"]["fullName"],
                player["person"]["link"],
                player["position"]["name"],
                player["position"]["type"],
                away_team_id,
                player["battingOrder"] if "battingOrder" in player else None,
                stats["flyOuts"],
                stats["groundOuts"],
                stats["airOuts"],
                stats["runs"],
                stats["rbi"],
                singles,
                stats["doubles"],
                stats["triples"],
                stats["homeRuns"],
                stats["strikeOuts"],
                stats["baseOnBalls"],
                stats["intentionalWalks"],
                stats["hits"],
                stats["hitByPitch"],
                stats["atBats"],
                stats["plateAppearances"],
                avg,
                obp,
                slg,
                ops,
                stats["caughtStealing"],
                stats["stolenBases"],
                stats["groundIntoDoublePlay"],
                stats["groundIntoTriplePlay"],
                stats["totalBases"],
                stats["leftOnBase"],
                stats["sacBunts"],
                stats["sacFlies"],
                stats["catchersInterference"],
                stats["pickoffs"],
                stats["popOuts"],
                stats["lineOuts"],
            )

            batters.append(batter_insert)

    for player_id in home_player_ids:
        player = data["teams"]["home"]["players"][player_id]

        if player["stats"]["batting"]:
            stats = player["stats"]["batting"]
            avg = stats["hits"] / stats["atBats"] if stats["atBats"] != 0 else None
            obp_numerator = stats["hits"] + stats["baseOnBalls"] + stats["hitByPitch"]
            obp_denominator = (
                stats["atBats"]
                + stats["baseOnBalls"]
                + stats["hitByPitch"]
                + stats["sacFlies"]
            )
            obp = obp_numerator / obp_denominator if obp_denominator != 0 else None
            slg = (
                stats["totalBases"] / stats["atBats"] if stats["atBats"] != 0 else None
            )
            ops = obp + slg if slg != None else obp
            singles = stats["hits"] - (
                stats["doubles"] + stats["triples"] + stats["homeRuns"]
            )

            batter_insert = (
                str(game_id) + "_" + str(player["person"]["id"]),
                player["person"]["id"],
                game_id,
                player["person"]["fullName"],
                player["person"]["link"],
                player["position"]["name"],
                player["position"]["type"],
                home_team_id,
                player["battingOrder"] if "battingOrder" in player else None,
                stats["flyOuts"],
                stats["groundOuts"],
                stats["airOuts"],
                stats["runs"],
                stats["rbi"],
                singles,
                stats["doubles"],
                stats["triples"],
                stats["homeRuns"],
                stats["strikeOuts"],
                stats["baseOnBalls"],
                stats["intentionalWalks"],
                stats["hits"],
                stats["hitByPitch"],
                stats["atBats"],
                stats["plateAppearances"],
                avg,
                obp,
                slg,
                ops,
                stats["caughtStealing"],
                stats["stolenBases"],
                stats["groundIntoDoublePlay"],
                stats["groundIntoTriplePlay"],
                stats["totalBases"],
                stats["leftOnBase"],
                stats["sacBunts"],
                stats["sacFlies"],
                stats["catchersInterference"],
                stats["pickoffs"],
                stats["popOuts"],
                stats["lineOuts"],
            )

            batters.append(batter_insert)

    return {"insert_format": insert_format, "boxscore_insert": batters}
