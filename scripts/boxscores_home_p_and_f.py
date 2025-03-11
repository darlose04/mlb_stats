import json
from tools import division_names
from tools import league_names


def home_team_pitching_and_fielding(game_id, data):
    insert_format = (
        "INSERT INTO team_boxscores_home_pitching_and_fielding "
        "(game_id,season,home_team,home_team_id,league,league_id,division,division_id,home_team_wins,home_team_losses,home_team_pitching_flyouts,home_team_pitching_groundouts,home_team_pitching_airouts,home_team_pitching_runs,home_team_pitching_singles,home_team_pitching_doubles,home_team_pitching_triples,home_team_pitching_homeruns,home_team_pitching_hits,home_team_pitching_strikeouts,home_team_pitching_walks,home_team_pitching_int_walks,home_team_pitching_hbp,home_team_pitching_baa,home_team_pitching_at_bats,home_team_pitching_obp,home_team_pitching_slg,home_team_pitching_ops,home_team_pitching_caught_stealing,home_team_pitching_stolen_bases,home_team_pitching_era,home_team_pitching_ip,home_team_pitching_save_opportunities,home_team_pitching_earned_runs,home_team_pitching_whip,home_team_pitching_batters_faced,home_team_pitching_outs,home_team_pitching_cg,home_team_pitching_shutouts,home_team_pitching_num_pitches,home_team_pitching_balls,home_team_pitching_strikes,home_team_pitching_strike_perc,home_team_pitching_balks,home_team_pitching_wild_pitches,home_team_pitching_pickoffs,home_team_pitching_groundouts_to_airouts,home_team_pitching_rbi,home_team_pitching_pitches_per_inning,home_team_pitching_runs_scored_per_9,home_team_pitching_homeruns_per_9,home_team_pitching_inherited_runners,home_team_pitching_inherited_runners_scored,home_team_pitching_catcher_int,home_team_pitching_gidp,home_team_pitching_gitp,home_team_pitching_plate_appearances,home_team_pitching_total_bases,home_team_pitching_lob,home_team_pitching_sac_bunts,home_team_pitching_sac_flies,home_team_pitching_passed_ball,home_team_pitching_popouts,home_team_pitching_lineouts,home_team_fielding_assists,home_team_fielding_putouts,home_team_fielding_errors,home_team_fielding_chances) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )

    home_team = data["teams"]["home"]
    team_info = home_team["team"]
    pitching_stats = home_team["teamStats"]["pitching"]
    fielding_stats = home_team["teamStats"]["fielding"]

    singles = pitching_stats["hits"] - (
        pitching_stats["doubles"]
        + pitching_stats["triples"]
        + pitching_stats["homeRuns"]
    )
    baa = round(pitching_stats["hits"] / pitching_stats["atBats"], 3)
    obp = float(pitching_stats["obp"])
    # total bases / at bats
    # just going to grab the stat from the opposite team's data
    slg = float(data["teams"]["away"]["teamStats"]["batting"]["slg"])
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
        data["teams"]["away"]["teamStats"]["batting"]["groundIntoDoublePlay"],
        data["teams"]["away"]["teamStats"]["batting"]["groundIntoTriplePlay"],
        data["teams"]["away"]["teamStats"]["batting"]["plateAppearances"],
        data["teams"]["away"]["teamStats"]["batting"]["totalBases"],
        data["teams"]["away"]["teamStats"]["batting"]["leftOnBase"],
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
