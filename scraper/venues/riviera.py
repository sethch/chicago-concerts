import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.rivieratheatre.com/events"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _parse_date(text):
    try:
        return datetime.strptime(text.strip(), "%B %d %Y").strftime("%Y-%m-%d")
    except ValueError:
        return ""


def get_artists() -> list[dict]:
    page = requests.get(URL, headers=HEADERS, verify=False)
    soup = BeautifulSoup(page.text, "html.parser")
    artists = []
    seen = set()
    for item in soup.find_all("div", class_="eventItem"):
        title = item.find("h3", class_="title")
        if title and title.a:
            name = title.a.text.strip()
            show_url = title.a.get("href", "")
            date_el = item.find("div", class_="date")
            show_date = _parse_date(date_el.get("aria-label", "")) if date_el else ""
            if name and name not in seen:
                artists.append({"name": name, "show_url": show_url, "date": show_date})
                seen.add(name)
    return artists
