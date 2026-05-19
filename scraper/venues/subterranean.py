import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

URL = "https://www.subt.net"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _parse_date(text):
    try:
        today = date.today()
        d = datetime.strptime(text.strip(), "%a %b %d").replace(year=today.year).date()
        if d < today:
            d = d.replace(year=today.year + 1)
        return d.strftime("%Y-%m-%d")
    except ValueError:
        return ""


def get_artists() -> list[dict]:
    page = requests.get(URL, headers=HEADERS, verify=False)
    soup = BeautifulSoup(page.text, "html.parser")
    artists = []
    seen = set()
    for tag in soup.find_all("p", class_="headliners"):
        name = tag.text.strip()
        show_url = ""
        parent = tag.parent
        for _ in range(5):
            if parent is None:
                break
            if parent.name == "a" and parent.get("href"):
                show_url = parent.get("href")
                break
            a = parent.find("a", href=True)
            if a:
                show_url = a.get("href", "")
                break
            parent = parent.parent
        date_el = tag.find_previous("p", class_="event-date")
        show_date = _parse_date(date_el.text) if date_el else ""
        if name and name not in seen:
            artists.append({"name": name, "show_url": show_url, "date": show_date})
            seen.add(name)
    return artists
