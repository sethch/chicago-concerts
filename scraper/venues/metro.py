import re
import requests
from bs4 import BeautifulSoup

URL = "https://metrochicago.com/events/"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_artists() -> list[dict]:
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.text, "html.parser")
    artists = []
    seen = set()
    for card in soup.find_all("div", class_="rhpSingleEvent"):
        a = card.find("a", class_="url")
        if not a:
            continue
        name = a.get("title", "").strip()
        show_url = a.get("href", "")
        name = re.split(r"\s*[:–-]\s*", name)[0].strip()
        name = re.split(r"\s+(?:with|feat|featuring|&|\+|w/)", name, flags=re.IGNORECASE)[0].strip()
        if name and name not in seen:
            artists.append({"name": name, "show_url": show_url})
            seen.add(name)
    return artists
