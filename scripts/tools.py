def get_ids(cursor, season):
    # May want to break this down season by season instead of all at once
    # TODO: will want to pass in parameters for year and maybe team
    get_game_ids = (
        f"select id from mlb.games where season = {season} order by game_date desc"
    )

    cursor.execute(
        get_game_ids,
    )

    game_ids = []

    for id in cursor:
        game_ids.append(id[0])

    return game_ids


def division_names():
    return {
        200: "American League West",
        201: "American League East",
        202: "American League Central",
        203: "National League West",
        204: "National League East",
        205: "National League Central",
    }


def league_names():
    return {103: "American League", 104: "National League"}


# TODO: going to need to make functions for the different team stats as well as the player stats
# will need to populate all the different tables for each api call to get game boxscore info since
# there are a lot of calls to make

# make call to get box score
# populate each table with the returning data
# make next call
# will probably need to only do a couple hundred at once? Maybe one team at a time.
# Since there is no documentation not really sure what is defined as bulk or what is or isn't 'allowed'
