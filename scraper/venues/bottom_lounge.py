import re
import requests
from bs4 import BeautifulSoup

URL = "https://bottomlounge.com/events/"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_artists() -> list[dict]:
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.text, "html.parser")
    artists = []
    seen = set()
    for art in soup.find_all("article"):
        h2 = art.find("h2", class_="w-post-elm")
        btn = art.find("a", class_="w-btn")
        if not h2:
            continue
        name = h2.get_text(strip=True)
        show_url = btn.get("href", "") if btn else ""
        name = name.split(",")[0].strip()
        name = re.split(r"\s+(?:with|feat|featuring|w/)", name, flags=re.IGNORECASE)[0].strip()
        name = re.split(r"\s*[–-]\s+", name)[0].strip()
        if name and name not in seen:
            artists.append({"name": name, "show_url": show_url})
            seen.add(name)
    return artists
