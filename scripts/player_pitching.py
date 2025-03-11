import json
import uuid


def player_pitching(game_id, data):
    insert_format = (
        "INSERT INTO player_pitching "
        "(id,player_id,game_id,name,link,position_name,position_type,team_id,starts,appearances,flyouts,groundouts,airouts,runs,rbi,singles,doubles,triples,homeruns,strikeouts,walks,intentional_walks,hits,hbp,at_bats,avg,obp,slg,ops,caught_stealing,stolen_bases,ip,wins,losses,saves,save_opportunities,holds,blown_saves,earned_runs,batters_faced,outs,complete_games,shutouts,pitch_count,balls,strikes,balks,wild_pitches,pickoffs,runs_per_9,homeruns_per_9,inherited_runners,inherited_runners_scored,catchers_int,sac_bunts,sac_flies,passed_ball,popouts,lineouts) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )

    pitchers = []

    away_player_ids = data["teams"]["away"]["players"].keys()
    home_player_ids = data["teams"]["home"]["players"].keys()
    away_team_id = data["teams"]["away"]["team"]["id"]
    home_team_id = data["teams"]["home"]["team"]["id"]

    for player_id in away_player_ids:
        player = data["teams"]["away"]["players"][player_id]

        if player["stats"]["pitching"]:
            stats = player["stats"]["pitching"]
            avg = stats["hits"] / stats["atBats"] if stats["atBats"] != 0 else None
            obp_numerator = stats["hits"] + stats["baseOnBalls"] + stats["hitByPitch"]
            obp_denominator = (
                stats["atBats"]
                + stats["baseOnBalls"]
                + stats["hitByPitch"]
                + stats["sacFlies"]
            )
            obp = obp_numerator / obp_denominator if obp_denominator != 0 else None
            singles = stats["hits"] - (
                stats["doubles"] + stats["triples"] + stats["homeRuns"]
            )
            total_bases = (
                (singles * 1)
                + (stats["doubles"] * 2)
                + (stats["triples"] * 3)
                + (stats["homeRuns"] * 4)
            )
            slg = total_bases / stats["atBats"] if stats["atBats"] != 0 else None
            ops = obp + slg if slg != None else obp
            relief_appearances = (
                stats["gamesPlayed"] if stats["gamesStarted"] == 0 else 0
            )
            ip = float(stats["inningsPitched"])
            rp9 = (
                float(stats["runsScoredPer9"])
                if stats["runsScoredPer9"] != "-.--"
                else 0.00
            )
            hrp9 = (
                float(stats["homeRunsPer9"])
                if stats["homeRunsPer9"] != "-.--"
                else 0.00
            )

            pitcher_insert = (
                str(game_id) + "_" + str(player["person"]["id"]),
                player["person"]["id"],
                game_id,
                player["person"]["fullName"],
                player["person"]["link"],
                player["position"]["name"],
                player["position"]["type"],
                away_team_id,
                stats["gamesStarted"],
                relief_appearances,
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
                avg,
                obp,
                slg,
                ops,
                stats["caughtStealing"],
                stats["stolenBases"],
                ip,
                stats["wins"],
                stats["losses"],
                stats["saves"],
                stats["saveOpportunities"],
                stats["holds"],
                stats["blownSaves"],
                stats["earnedRuns"],
                stats["battersFaced"],
                stats["outs"],
                stats["completeGames"],
                stats["shutouts"],
                stats["pitchesThrown"] if "pitchesThrown" in stats else 0,
                stats["balls"],
                stats["strikes"],
                stats["balks"],
                stats["wildPitches"],
                stats["pickoffs"],
                rp9,
                hrp9,
                stats["inheritedRunners"],
                stats["inheritedRunnersScored"],
                stats["catchersInterference"],
                stats["sacBunts"],
                stats["sacFlies"],
                stats["passedBall"],
                stats["popOuts"],
                stats["lineOuts"],
            )

            pitchers.append(pitcher_insert)

    for player_id in home_player_ids:
        player = data["teams"]["home"]["players"][player_id]

        if player["stats"]["pitching"]:
            stats = player["stats"]["pitching"]
            avg = stats["hits"] / stats["atBats"] if stats["atBats"] != 0 else None
            obp_numerator = stats["hits"] + stats["baseOnBalls"] + stats["hitByPitch"]
            obp_denominator = (
                stats["atBats"]
                + stats["baseOnBalls"]
                + stats["hitByPitch"]
                + stats["sacFlies"]
            )
            obp = obp_numerator / obp_denominator if obp_denominator != 0 else None
            singles = stats["hits"] - (
                stats["doubles"] + stats["triples"] + stats["homeRuns"]
            )
            total_bases = (
                (singles * 1)
                + (stats["doubles"] * 2)
                + (stats["triples"] * 3)
                + (stats["homeRuns"] * 4)
            )
            slg = total_bases / stats["atBats"] if stats["atBats"] != 0 else None
            ops = obp + slg if slg != None else obp

            relief_appearances = (
                stats["gamesPlayed"] if stats["gamesStarted"] == 0 else 0
            )
            ip = float(stats["inningsPitched"])
            rp9 = (
                float(stats["runsScoredPer9"])
                if stats["runsScoredPer9"] != "-.--"
                else 0.00
            )
            hrp9 = (
                float(stats["homeRunsPer9"])
                if stats["homeRunsPer9"] != "-.--"
                else 0.00
            )

            pitcher_insert = (
                str(game_id) + "_" + str(player["person"]["id"]),
                player["person"]["id"],
                game_id,
                player["person"]["fullName"],
                player["person"]["link"],
                player["position"]["name"],
                player["position"]["type"],
                home_team_id,
                stats["gamesStarted"],
                relief_appearances,
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
                avg,
                obp,
                slg,
                ops,
                stats["caughtStealing"],
                stats["stolenBases"],
                ip,
                stats["wins"],
                stats["losses"],
                stats["saves"],
                stats["saveOpportunities"],
                stats["holds"],
                stats["blownSaves"],
                stats["earnedRuns"],
                stats["battersFaced"],
                stats["outs"],
                stats["completeGames"],
                stats["shutouts"],
                stats["pitchesThrown"] if "pitchesThrown" in stats else 0,
                stats["balls"],
                stats["strikes"],
                stats["balks"],
                stats["wildPitches"],
                stats["pickoffs"],
                rp9,
                hrp9,
                stats["inheritedRunners"],
                stats["inheritedRunnersScored"],
                stats["catchersInterference"],
                stats["sacBunts"],
                stats["sacFlies"],
                stats["passedBall"],
                stats["popOuts"],
                stats["lineOuts"],
            )

            pitchers.append(pitcher_insert)

    return {"insert_format": insert_format, "boxscore_insert": pitchers}
