import json
from tools import division_names
from tools import league_names


def away_team_pitching_and_fielding(game_id, data):
    insert_format = (
        "INSERT INTO team_boxscores_away_pitching_and_fielding "
        "(game_id,season,away_team,away_team_id,league,league_id,division,division_id,away_team_wins,away_team_losses,away_team_pitching_flyouts,away_team_pitching_groundouts,away_team_pitching_airouts,away_team_pitching_runs,away_team_pitching_singles,away_team_pitching_doubles,away_team_pitching_triples,away_team_pitching_homeruns,away_team_pitching_hits,away_team_pitching_strikeouts,away_team_pitching_walks,away_team_pitching_int_walks,away_team_pitching_hbp,away_team_pitching_baa,away_team_pitching_at_bats,away_team_pitching_obp,away_team_pitching_slg,away_team_pitching_ops,away_team_pitching_caught_stealing,away_team_pitching_stolen_bases,away_team_pitching_era,away_team_pitching_ip,away_team_pitching_save_opportunities,away_team_pitching_earned_runs,away_team_pitching_whip,away_team_pitching_batters_faced,away_team_pitching_outs,away_team_pitching_cg,away_team_pitching_shutouts,away_team_pitching_num_pitches,away_team_pitching_balls,away_team_pitching_strikes,away_team_pitching_strike_perc,away_team_pitching_balks,away_team_pitching_wild_pitches,away_team_pitching_pickoffs,away_team_pitching_groundouts_to_airouts,away_team_pitching_rbi,away_team_pitching_pitches_per_inning,away_team_pitching_runs_scored_per_9,away_team_pitching_homeruns_per_9,away_team_pitching_inherited_runners,away_team_pitching_inherited_runners_scored,away_team_pitching_catcher_int,away_team_pitching_gidp,away_team_pitching_gitp,away_team_pitching_plate_appearances,away_team_pitching_total_bases,away_team_pitching_lob,away_team_pitching_sac_bunts,away_team_pitching_sac_flies,away_team_pitching_passed_ball,away_team_pitching_popouts,away_team_pitching_lineouts,away_team_fielding_assists,away_team_fielding_putouts,away_team_fielding_errors,away_team_fielding_chances) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )

    away_team = data["teams"]["away"]
    team_info = away_team["team"]
    pitching_stats = away_team["teamStats"]["pitching"]
    fielding_stats = away_team["teamStats"]["fielding"]

    singles = pitching_stats["hits"] - (
        pitching_stats["doubles"]
        + pitching_stats["triples"]
        + pitching_stats["homeRuns"]
    )
    baa = round(pitching_stats["hits"] / pitching_stats["atBats"], 3)
    obp = float(pitching_stats["obp"])
    # total bases / at bats
    # just going to grab the stat from the opposite team's data
    slg = float(data["teams"]["home"]["teamStats"]["batting"]["slg"])
    ops = obp + slg
    era = float(pitching_stats["era"])
    ip = float(pitching_stats["inningsPitched"])
    whip = float(pitching_stats["whip"])
    kPerc = float(pitching_stats["strikePercentage"])
    groundouts_to_airouts = float(pitching_stats["groundOutsToAirouts"])
    ppi = float(pitching_stats["pitchesPerInning"])
    runs_per_nine = float(pitching_stats["runsScoredPer9"])
    homeruns_per_nine = float(pitching_stats["homeRunsPer9"])

    division_dict = division_names()
    league_dict = league_names()

    boxscore_insert = (
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
        pitching_stats["flyOuts"],
        pitching_stats["groundOuts"],
        pitching_stats["airOuts"],
        pitching_stats["runs"],
        singles,
        pitching_stats["doubles"],
        pitching_stats["triples"],
        pitching_stats["homeRuns"],
        pitching_stats["hits"],
        pitching_stats["strikeOuts"],
        pitching_stats["baseOnBalls"],
        pitching_stats["intentionalWalks"],
        pitching_stats["hitByPitch"],
        baa,
        pitching_stats["atBats"],
        obp,
        slg,
        ops,
        pitching_stats["caughtStealing"],
        pitching_stats["stolenBases"],
        era,
        ip,
        pitching_stats["saveOpportunities"],
        pitching_stats["earnedRuns"],
        whip,
        pitching_stats["battersFaced"],
        pitching_stats["outs"],
        pitching_stats["completeGames"],
        pitching_stats["shutouts"],
        pitching_stats["numberOfPitches"],
        pitching_stats["balls"],
        pitching_stats["strikes"],
        kPerc,
        pitching_stats["balks"],
        pitching_stats["wildPitches"],
        pitching_stats["pickoffs"],
        groundouts_to_airouts,
        pitching_stats["rbi"],
        ppi,
        runs_per_nine,
        homeruns_per_nine,
        pitching_stats["inheritedRunners"],
        pitching_stats["inheritedRunnersScored"],
        pitching_stats["catchersInterference"],
        data["teams"]["home"]["teamStats"]["batting"]["groundIntoDoublePlay"],
        data["teams"]["home"]["teamStats"]["batting"]["groundIntoTriplePlay"],
        data["teams"]["home"]["teamStats"]["batting"]["plateAppearances"],
        data["teams"]["home"]["teamStats"]["batting"]["totalBases"],
        data["teams"]["home"]["teamStats"]["batting"]["leftOnBase"],
        pitching_stats["sacBunts"],
        pitching_stats["sacFlies"],
        pitching_stats["passedBall"],
        pitching_stats["popOuts"],
        pitching_stats["lineOuts"],
        fielding_stats["assists"],
        fielding_stats["putOuts"],
        fielding_stats["errors"],
        fielding_stats["chances"],
    )

    return {"insert_format": insert_format, "boxscore_insert": list(boxscore_insert)}
