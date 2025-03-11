import json
import uuid
from tools import division_names
from tools import league_names


def away_team_batting(game_id, data):
    # use uuid for unique id
    insert_format = (
        "INSERT INTO team_boxscores_away_batting "
        "(game_id,season,away_team,away_team_id,league,league_id,division,division_id,away_team_wins,away_team_losses,away_team_batting_flyouts,away_team_batting_groundouts,away_team_batting_airouts,away_team_batting_runs,away_team_batting_singles,away_team_batting_doubles,away_team_batting_triples,away_team_batting_homeruns,away_team_batting_hits,away_team_batting_strikeouts,away_team_batting_walks,away_team_batting_int_walks,away_team_batting_hbp,away_team_batting_avg,away_team_batting_at_bats,away_team_batting_obp,away_team_batting_slg,away_team_batting_ops,away_team_batting_caught_stealing,away_team_batting_stolen_bases,away_team_batting_gidp,away_team_batting_gitp,away_team_batting_plate_appearances,away_team_batting_total_bases,away_team_batting_rbi,away_team_batting_lob,away_team_batting_sac_bunts,away_team_batting_sac_flies,away_team_batting_catcher_int,away_team_batting_pickoffs,away_team_batting_popouts,away_team_batting_lineouts) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )

    away_team = data["teams"]["away"]
    team_info = away_team["team"]
    stats = away_team["teamStats"]["batting"]
    unique_id = str(uuid.uuid4())
    avg = float(stats["avg"])
    obp = float(stats["obp"])
    slg = float(stats["slg"])
    ops = float(stats["ops"])

    division_dict = division_names()
    league_dict = league_names()

    boxscore_insert = (
        # unique_id,
        game_id,
        team_info["season"],
        team_info["name"],
        team_info["id"],
        league_dict[team_info["league"]["id"]],
        team_info["league"]["id"],
        division_dict[team_info["division"]["id"]],
        team_info["division"]["id"],
        team_info["record"]["leagueRecord"]["wins"],
        team_info["record"]["leagueRecord"]["losses"],
        stats["flyOuts"],
        stats["groundOuts"],
        stats["airOuts"],
        stats["runs"],
        stats["hits"] - (stats["doubles"] + stats["triples"] + stats["homeRuns"]),
        stats["doubles"],
        stats["triples"],
        stats["homeRuns"],
        stats["hits"],
        stats["strikeOuts"],
        stats["baseOnBalls"],
        stats["intentionalWalks"],
        stats["hitByPitch"],
        avg,
        stats["atBats"],
        obp,
        slg,
        ops,
        stats["caughtStealing"],
        stats["stolenBases"],
        stats["groundIntoDoublePlay"],
        stats["groundIntoTriplePlay"],
        stats["plateAppearances"],
        stats["totalBases"],
        stats["rbi"],
        stats["leftOnBase"],
        stats["sacBunts"],
        stats["sacFlies"],
        stats["catchersInterference"],
        stats["pickoffs"],
        stats["popOuts"],
        stats["lineOuts"],
    )

    return {"insert_format": insert_format, "boxscore_insert": list(boxscore_insert)}
