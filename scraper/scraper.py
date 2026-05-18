import json
import os
from datetime import datetime, timezone
from pathlib import Path

from spotify import update_playlist
from venues import schubas, empty_bottle, thalia_hall, riviera, subterranean, salt_shed, metro, bottom_lounge, aragon, soldier_field, wrigley_field, northerly_island, united_center

VENUES = [
    ("Schubas / Lincoln Hall",              schubas.get_artists,        "SPOTIFY_SCHUBAS_PLAYLIST_ID",        "https://www.lh-st.com/shows/"),
    ("Empty Bottle",                        empty_bottle.get_artists,   "SPOTIFY_EMPTY_BOTTLE_PLAYLIST_ID",   "https://www.emptybottle.com"),
    ("Thalia Hall",                         thalia_hall.get_artists,    "SPOTIFY_THALIA_HALL_PLAYLIST_ID",    "https://www.thaliahallchicago.com"),
    ("Riviera",                             riviera.get_artists,        "SPOTIFY_RIVIERA_PLAYLIST_ID",        "https://www.rivieratheatre.com/events"),
    ("Subterranean",                        subterranean.get_artists,   "SPOTIFY_SUBTERRANEAN_PLAYLIST_ID",   "https://www.subt.net"),
    ("Salt Shed",                           salt_shed.get_artists,      "SPOTIFY_SALT_SHED_PLAYLIST_ID",      "https://www.saltshedchicago.com/home#shows"),
    ("Metro",                               metro.get_artists,          "SPOTIFY_METRO_PLAYLIST_ID",          "https://metrochicago.com/events/"),
    ("Bottom Lounge",                       bottom_lounge.get_artists,  "SPOTIFY_BOTTOM_LOUNGE_PLAYLIST_ID",  "https://bottomlounge.com/events/"),
    ("Aragon Ballroom",                     aragon.get_artists,         "SPOTIFY_ARAGON_PLAYLIST_ID",         "https://www.aragonballroomchicago.com/shows"),
    ("Soldier Field",                       soldier_field.get_artists,  "SPOTIFY_SOLDIER_FIELD_PLAYLIST_ID",  "https://www.soldierfield.com/events"),
    ("Wrigley Field",                       wrigley_field.get_artists,  "SPOTIFY_WRIGLEY_FIELD_PLAYLIST_ID",  "https://www.wrigleyfield.com/concerts"),
    ("Northerly Island",                    northerly_island.get_artists, "SPOTIFY_NORTHERLY_ISLAND_PLAYLIST_ID", "https://www.huntingtonbankpavilion.com"),
    ("United Center",                       united_center.get_artists,   "SPOTIFY_UNITED_CENTER_PLAYLIST_ID",   "https://www.unitedcenter.com/events/"),
]

MANIFEST_PATH = Path(__file__).parent.parent / "docs" / "data.json"


def main():
    all_artists = []

    for name, get_artists, playlist_env, venue_url in VENUES:
        playlist_id = os.environ.get(playlist_env)
        if not playlist_id:
            print(f"Skipping {name}: {playlist_env} not set")
            continue
        print(f"\n=== {name} ===")
        try:
            artists = get_artists()
            artist_names = [a["name"] for a in artists]
            print(f"Found {len(artists)} artists: {artist_names}")
            metadata = update_playlist(artist_names, playlist_id)
            print(f"Playlist updated.")
            meta_by_name = {m["name"]: m for m in metadata}
            for artist in artists:
                m = meta_by_name.get(artist["name"], {})
                all_artists.append({
                    "name": artist["name"],
                    "venue": name,
                    "venue_url": venue_url,
                    "show_url": artist.get("show_url", ""),
                    "date": artist.get("date", ""),
                    "spotify_url": m.get("spotify_url", ""),
                    "genres": m.get("genres", []),
                    "popularity": m.get("popularity", 0),
                })
        except Exception as e:
            print(f"Error processing {name}: {e}")

    manifest = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "artists": all_artists,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    print(f"\nWrote {len(all_artists)} artists to {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
