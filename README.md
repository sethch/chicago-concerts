# Chicago Concerts

A static site that tracks upcoming shows at Chicago music venues. Every Monday a GitHub Actions job scrapes each venue, updates per-venue Spotify playlists with each artist's top 3 tracks, and writes a `data.json` manifest. The site is hosted on GitHub Pages.

**Live site:** https://sethch.github.io/chicago-concerts/

## Features

- **Search** — fuzzy search across all artists and venues (Fuse.js)
- **Browse tab** — filter by genre (scrollable chip row) and popularity slider; scrollable artist grid
- **For You tab** — personalized picks two ways:
  - Connect Spotify (PKCE OAuth, no backend required) to match your listening history against upcoming shows
  - Add artists you like manually; genre-based matching surfaces similar acts at Chicago venues
  - Seeds persist in `localStorage`
- **Venue playlists** — embedded Spotify iframes for each venue, updated weekly

## Venues

| Venue | Scraper method |
|---|---|
| Schubas / Lincoln Hall | requests + BeautifulSoup |
| Empty Bottle | Selenium (JS-rendered) |
| Thalia Hall | Selenium (JS-rendered) |
| Riviera Theatre | requests + BeautifulSoup |
| Subterranean | requests + BeautifulSoup |
| Salt Shed | Selenium (Ticketmaster widget) |

### Venues to add

- Bottom Lounge
- Metro
- Aragon Ballroom

## Structure

```
scraper/
  venues/          One module per venue, each exports get_artists() -> list[str]
  scraper.py       Main entry; scrapes venues, updates playlists, writes docs/data.json
  spotify.py       Spotify client (refresh token auth) + playlist updater
  requirements.txt
docs/
  index.html       Single-page static site
  data.json        Artist manifest written by scraper (updated weekly)
.github/workflows/scrape.yml   Monday noon UTC cron + workflow_dispatch
```

## Secrets (GitHub Actions)

| Secret | Description |
|---|---|
| `SPOTIFY_CLIENT_ID` | Spotify app client ID |
| `SPOTIFY_CLIENT_SECRET` | Spotify app client secret |
| `SPOTIFY_REFRESH_TOKEN` | Long-lived refresh token (one-time manual OAuth) |
| `SPOTIFY_SCHUBAS_PLAYLIST_ID` | Playlist ID for each venue (×6) |
| `SPOTIFY_EMPTY_BOTTLE_PLAYLIST_ID` | |
| `SPOTIFY_THALIA_HALL_PLAYLIST_ID` | |
| `SPOTIFY_RIVIERA_PLAYLIST_ID` | |
| `SPOTIFY_SUBTERRANEAN_PLAYLIST_ID` | |
| `SPOTIFY_SALT_SHED_PLAYLIST_ID` | |

To run locally: export the above as environment variables, then `python scraper/scraper.py`.

## Spotify PKCE note

The "Connect Spotify" button uses the PKCE OAuth flow — no backend required. The redirect URI `https://sethch.github.io/chicago-concerts/` must be registered in the Spotify Developer Dashboard under the app's allowed redirect URIs.
