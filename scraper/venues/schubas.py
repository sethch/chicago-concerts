import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

URL = "https://www.lh-st.com/shows/"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _parse_date(text):
    try:
        today = date.today()
        d = datetime.strptime(text.strip(), "%b %d").replace(year=today.year).date()
        if d < today:
            d = d.replace(year=today.year + 1)
        return d.strftime("%Y-%m-%d")
    except ValueError:
        return ""


def _parse_venue(text):
    t = text.strip()
    if "Lincoln Hall" in t:
        return "Lincoln Hall"
    return "Schubas"


def get_artists() -> list[dict]:
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.text, "html.parser")
    artists = []
    seen = set()
    for card in soup.find_all("div", class_="card-body"):
        title = card.find("h4", class_="card-title")
        if title:
            name = title.text.strip()
            link = card.find("a")
            show_url = link["href"] if link else ""
            date_el = card.find("span", class_="date")
            show_date = _parse_date(date_el.text) if date_el else ""
            # Find venue name in card footer
            card_el = card.parent
            venue_el = card_el.find("span", class_="tessera-venue") if card_el else None
            venue = _parse_venue(venue_el.text) if venue_el else "Schubas"
            if name and name not in seen:
                artists.append({"name": name, "show_url": show_url, "date": show_date, "venue": venue})
                seen.add(name)
    return artists
