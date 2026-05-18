import os
import requests

BASE = "https://app.ticketmaster.com/discovery/v2"


def get_artists(*venue_ids: str) -> list[dict]:
    api_key = os.environ.get("TICKETMASTER_API_KEY")
    if not api_key:
        raise RuntimeError("TICKETMASTER_API_KEY not set")

    artists = []
    seen = set()

    for venue_id in venue_ids:
        page = 0
        while True:
            r = requests.get(f"{BASE}/events.json", params={
                "venueId": venue_id,
                "classificationName": "music",
                "size": 50,
                "page": page,
                "apikey": api_key,
            })
            data = r.json()
            events = data.get("_embedded", {}).get("events", [])
            if not events:
                break

            for event in events:
                attrs = event.get("_embedded", {}).get("attractions", [])
                name = attrs[0]["name"] if attrs else event.get("name", "")
                show_url = event.get("url", "")
                if name and name not in seen:
                    artists.append({"name": name, "show_url": show_url})
                    seen.add(name)

            total_pages = data.get("page", {}).get("totalPages", 1)
            if page >= total_pages - 1:
                break
            page += 1

    return artists
