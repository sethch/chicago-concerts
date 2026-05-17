import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def _client() -> spotipy.Spotify:
    auth_manager = SpotifyOAuth(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri="http://localhost:4200/callback",
        scope="playlist-modify-public playlist-modify-private",
        open_browser=False,
    )
    token_info = auth_manager.refresh_access_token(os.environ["SPOTIFY_REFRESH_TOKEN"])
    return spotipy.Spotify(auth=token_info["access_token"])


def update_playlist(artists: list[str], playlist_id: str) -> None:
    sp = _client()
    sp.playlist_replace_items(playlist_id, [])

    track_ids = []
    for name in artists:
        if not name:
            continue
        result = sp.search(q=name, type="artist")
        items = result.get("artists", {}).get("items", [])
        if not items:
            continue

        name_lower = name.lower()
        match = next(
            (a for a in items if name_lower in a.get("name", "").lower()), None
        )
        if not match:
            continue

        top_tracks = sp.artist_top_tracks(match["id"]).get("tracks", [])[:3]
        track_ids.extend(t["id"] for t in top_tracks if t.get("id"))

    # Spotify API limit: 100 tracks per request
    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(playlist_id=playlist_id, items=track_ids[i : i + 100])
        print(f"Added {len(track_ids[i:i+100])} tracks to {playlist_id}")
