import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

URL = "https://metrochicago.com/events/"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _parse_date(text):
    try:
        today = date.today()
        d = datetime.strptime(text.strip(), "%a, %b %d").replace(year=today.year).date()
        if d < today:
            d = d.replace(year=today.year + 1)
        return d.strftime("%Y-%m-%d")
    except ValueError:
        return ""


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
        date_el = card.find(class_="singleEventDate")
        show_date = _parse_date(date_el.text) if date_el else ""
        if name and name not in seen:
            artists.append({"name": name, "show_url": show_url, "date": show_date})
            seen.add(name)
    return artists
