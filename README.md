# Chicago Concerts

A static site that tracks upcoming shows at Chicago music venues. Every Monday a GitHub Actions job scrapes each venue, updates per-venue Spotify playlists with each artist's top 3 tracks, and writes a `data.json` manifest. The site is hosted on GitHub Pages.

**Live site:** https://sethch.github.io/chicago-concerts/

## Features

- **Search** — fuzzy search across all artists and venues (Fuse.js); click a result to open the show page
- **Browse tab** — artists grouped by concert date; filter by venue and genre chips
- **For You tab** — personalized picks two ways:
  - Connect Spotify (PKCE OAuth, no backend required) to match your listening history against upcoming shows
  - Add artists manually; genre-based matching surfaces similar acts
  - Seeds persist in `localStorage`
- **Venue playlists** — collapsible accordion of embedded Spotify iframes (lazy-loaded on expand), one per venue

## Venues

| Venue | Scraper method |
|---|---|
| Schubas / Lincoln Hall | requests + BeautifulSoup |
| Empty Bottle | Ticketmaster Discovery API |
| Thalia Hall | Ticketmaster Discovery API |
| Riviera Theatre | requests + BeautifulSoup |
| Subterranean | requests + BeautifulSoup |
| Salt Shed | Ticketmaster Discovery API |
| Metro | requests + BeautifulSoup |
| Bottom Lounge | Ticketmaster Discovery API |
| Aragon Ballroom | Ticketmaster Discovery API |
| Soldier Field | Ticketmaster Discovery API |
| Wrigley Field | Ticketmaster Discovery API |
| Northerly Island | Ticketmaster Discovery API |
| United Center | Ticketmaster Discovery API |

## Structure

```
scraper/
  venues/          One module per venue, each exports get_artists() -> list[dict]
  venues/ticketmaster.py   Shared Ticketmaster API client (pagination, dedup, dates)
  scraper.py       Main entry; scrapes venues, updates playlists, writes docs/data.json
  spotify.py       Spotify client (refresh token auth) + playlist updater
  requirements.txt
docs/
  index.html       Single-page static site (vanilla JS, no framework)
  data.json        Artist manifest written by scraper (updated weekly)
.github/workflows/scrape.yml   Monday noon UTC cron + workflow_dispatch
```

### `data.json` schema

Each entry in `artists` has:

```json
{
  "name": "Artist Name",
  "venue": "Venue Name",
  "venue_url": "https://...",
  "show_url": "https://...",
  "date": "2026-05-25",
  "spotify_url": "https://open.spotify.com/artist/...",
  "genres": ["indie rock", "dream pop"],
  "popularity": 62
}
```

## Secrets (GitHub Actions)

| Secret | Description |
|---|---|
| `SPOTIFY_CLIENT_ID` | Spotify app client ID |
| `SPOTIFY_CLIENT_SECRET` | Spotify app client secret |
| `SPOTIFY_REFRESH_TOKEN` | Long-lived refresh token (one-time manual OAuth) |
| `TICKETMASTER_API_KEY` | Ticketmaster Discovery API consumer key |
| `SPOTIFY_SCHUBAS_PLAYLIST_ID` | Playlist ID for each venue (×13) |
| `SPOTIFY_EMPTY_BOTTLE_PLAYLIST_ID` | |
| `SPOTIFY_THALIA_HALL_PLAYLIST_ID` | |
| `SPOTIFY_RIVIERA_PLAYLIST_ID` | |
| `SPOTIFY_SUBTERRANEAN_PLAYLIST_ID` | |
| `SPOTIFY_SALT_SHED_PLAYLIST_ID` | |
| `SPOTIFY_METRO_PLAYLIST_ID` | |
| `SPOTIFY_BOTTOM_LOUNGE_PLAYLIST_ID` | |
| `SPOTIFY_ARAGON_PLAYLIST_ID` | |
| `SPOTIFY_SOLDIER_FIELD_PLAYLIST_ID` | |
| `SPOTIFY_WRIGLEY_FIELD_PLAYLIST_ID` | |
| `SPOTIFY_NORTHERLY_ISLAND_PLAYLIST_ID` | |
| `SPOTIFY_UNITED_CENTER_PLAYLIST_ID` | |

To run locally: export the above as environment variables, then `python scraper/scraper.py`.

## Spotify PKCE note

The "Connect Spotify" button uses the PKCE OAuth flow — no backend required. The redirect URI `https://sethch.github.io/chicago-concerts/` must be registered in the Spotify Developer Dashboard under the app's allowed redirect URIs.
