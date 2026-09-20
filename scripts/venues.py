"""Populate the `venues` table from the MLB Stats API.

Every venue id referenced by games, scheduled_games or teams is fetched (in
one batched call) with location, field and timezone info, and upserted. Venue
ids are stable through renames (PacBell -> SBC -> AT&T -> Oracle Park is one
id), so this holds the *current* name and metadata; historical names live on
the per-game rows in `games.venue_name`.

Run after games.py in updateDB.sh so newly scheduled neutral sites show up.
"""

import requests
from dotenv import load_dotenv
from db import get_connection

load_dotenv()

API = "https://statsapi.mlb.com/api/v1/venues"

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS {schema}.venues (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    state TEXT,
    state_abbrev TEXT,
    country TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    elevation INTEGER,
    azimuth DOUBLE PRECISION,
    timezone TEXT,
    capacity INTEGER,
    turf_type TEXT,
    roof_type TEXT,
    left_line INTEGER,
    left_center INTEGER,
    center INTEGER,
    right_center INTEGER,
    right_line INTEGER,
    active BOOLEAN,
    updated_at TIMESTAMP NOT NULL DEFAULT now()
)
"""

UPSERT_SQL = """
INSERT INTO {schema}.venues
    (id, name, city, state, state_abbrev, country, latitude, longitude, elevation,
     azimuth, timezone, capacity, turf_type, roof_type,
     left_line, left_center, center, right_center, right_line, active, updated_at)
VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    city = EXCLUDED.city,
    state = EXCLUDED.state,
    state_abbrev = EXCLUDED.state_abbrev,
    country = EXCLUDED.country,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude,
    elevation = EXCLUDED.elevation,
    azimuth = EXCLUDED.azimuth,
    timezone = EXCLUDED.timezone,
    capacity = EXCLUDED.capacity,
    turf_type = EXCLUDED.turf_type,
    roof_type = EXCLUDED.roof_type,
    left_line = EXCLUDED.left_line,
    left_center = EXCLUDED.left_center,
    center = EXCLUDED.center,
    right_center = EXCLUDED.right_center,
    right_line = EXCLUDED.right_line,
    active = EXCLUDED.active,
    updated_at = now()
"""

VENUE_IDS_SQL = """
SELECT DISTINCT venue_id FROM (
    SELECT venue_id FROM games
    UNION SELECT venue_id FROM scheduled_games
    UNION SELECT venue_id FROM teams
) v WHERE venue_id IS NOT NULL ORDER BY venue_id
"""


def fetch_venues(ids, batch=100):
    """Yield venue dicts from the API, `batch` ids per request."""
    for i in range(0, len(ids), batch):
        chunk = ids[i : i + batch]
        params = {
            "venueIds": ",".join(str(v) for v in chunk),
            "hydrate": "location,fieldInfo,timezone",
        }
        resp = requests.get(API, params=params, timeout=30)
        resp.raise_for_status()
        yield from resp.json().get("venues", [])


def to_row(v):
    loc = v.get("location") or {}
    coords = loc.get("defaultCoordinates") or {}
    field = v.get("fieldInfo") or {}
    tz = v.get("timeZone") or {}
    return (
        v["id"],
        v["name"],
        loc.get("city"),
        loc.get("state"),
        loc.get("stateAbbrev"),
        loc.get("country"),
        coords.get("latitude"),
        coords.get("longitude"),
        loc.get("elevation"),
        loc.get("azimuthAngle"),
        tz.get("id"),
        field.get("capacity"),
        field.get("turfType"),
        field.get("roofType"),
        field.get("leftLine"),
        field.get("leftCenter"),
        field.get("center"),
        field.get("rightCenter"),
        field.get("rightLine"),
        v.get("active"),
    )


def main():
    cnx = get_connection()
    print("connected to db")
    cursor = cnx.cursor()
    try:
        for schema in ("public", "fantasy"):
            cursor.execute(CREATE_SQL.format(schema=schema))
        cnx.commit()

        cursor.execute(VENUE_IDS_SQL)
        ids = [r[0] for r in cursor.fetchall()]
        print(f"{len(ids)} venue ids referenced in the database")

        rows = [to_row(v) for v in fetch_venues(ids)]
        missing = set(ids) - {r[0] for r in rows}
        if missing:
            print(f"WARNING: MLB returned nothing for venue ids {sorted(missing)}")

        for schema in ("public", "fantasy"):
            cursor.executemany(UPSERT_SQL.format(schema=schema), rows)
        cnx.commit()
        print(f"Upserted {len(rows)} venues")
    except Exception as err:
        cnx.rollback()
        print(f"ERROR: {err}")
        raise
    finally:
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    main()
