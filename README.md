# Chicago Concerts

Scrapes upcoming shows from Chicago music venues and auto-populates per-venue Spotify playlists with each artist's top 3 tracks. A static website displays the playlists.

## Venues

- Schubas / Lincoln Hall
- Empty Bottle
- Thalia Hall
- Riviera
- Subterranean
- Salt Shed

## Structure

```
scraper/          Python scrapers + Spotify updater
scraper/venues/   One module per venue, each exports get_artists()
web/              Static HTML/CSS/JS website
.github/workflows/scrape.yml  Weekly cron job
```

## Setup

See `scraper/README.md` for scraper setup and Spotify credentials.
