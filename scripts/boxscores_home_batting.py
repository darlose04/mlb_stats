import json
import uuid
from tools import division_names
from tools import league_names


def home_team_batting(game_id, data):
    # use uuid for unique id
    insert_format = (
        "INSERT INTO team_boxscores_home_batting "
        "(game_id,season,home_team,home_team_id,league,league_id,division,division_id,home_team_wins,home_team_losses,home_team_batting_flyouts,home_team_batting_groundouts,home_team_batting_airouts,home_team_batting_runs,home_team_batting_singles,home_team_batting_doubles,home_team_batting_triples,home_team_batting_homeruns,home_team_batting_hits,home_team_batting_strikeouts,home_team_batting_walks,home_team_batting_int_walks,home_team_batting_hbp,home_team_batting_avg,home_team_batting_at_bats,home_team_batting_obp,home_team_batting_slg,home_team_batting_ops,home_team_batting_caught_stealing,home_team_batting_stolen_bases,home_team_batting_gidp,home_team_batting_gitp,home_team_batting_plate_appearances,home_team_batting_total_bases,home_team_batting_rbi,home_team_batting_lob,home_team_batting_sac_bunts,home_team_batting_sac_flies,home_team_batting_catcher_int,home_team_batting_pickoffs,home_team_batting_popouts,home_team_batting_lineouts) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )

    home_team = data["teams"]["home"]
    team_info = home_team["team"]
    stats = home_team["teamStats"]["batting"]
    unique_id = str(uuid.uuid4())
    avg = float(stats["avg"])
    obp = float(stats["obp"])
    slg = float(stats["slg"])
    ops = float(stats["ops"])

    division_dict = division_names()
    league_dict = league_names()

    # print(stats)
    # try and loop through keys for other files and refactoring
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
