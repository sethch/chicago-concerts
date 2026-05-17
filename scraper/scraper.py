import os
from spotify import update_playlist
from venues import schubas, empty_bottle, thalia_hall, riviera, subterranean, salt_shed

VENUES = [
    ("Schubas / Lincoln Hall", schubas.get_artists,      "SPOTIFY_SCHUBAS_PLAYLIST_ID"),
    ("Empty Bottle",           empty_bottle.get_artists,  "SPOTIFY_EMPTY_BOTTLE_PLAYLIST_ID"),
    ("Thalia Hall",            thalia_hall.get_artists,   "SPOTIFY_THALIA_HALL_PLAYLIST_ID"),
    ("Riviera",                riviera.get_artists,       "SPOTIFY_RIVIERA_PLAYLIST_ID"),
    ("Subterranean",           subterranean.get_artists,  "SPOTIFY_SUBTERRANEAN_PLAYLIST_ID"),
    ("Salt Shed",              salt_shed.get_artists,     "SPOTIFY_SALT_SHED_PLAYLIST_ID"),
]


def main():
    for name, get_artists, playlist_env in VENUES:
        playlist_id = os.environ.get(playlist_env)
        if not playlist_id:
            print(f"Skipping {name}: {playlist_env} not set")
            continue
        print(f"\n=== {name} ===")
        try:
            artists = get_artists()
            print(f"Found {len(artists)} artists: {artists}")
            update_playlist(artists, playlist_id)
            print(f"Playlist updated.")
        except Exception as e:
            print(f"Error processing {name}: {e}")


if __name__ == "__main__":
    main()
