import requests
from bs4 import BeautifulSoup

URL = "https://www.lh-st.com/shows/"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_artists() -> list[str]:
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.text, "html.parser")
    artists = []
    seen = set()
    for card in soup.find_all("div", class_="card-body"):
        title = card.find("h4", class_="card-title")
        if title:
            name = title.text.strip()
            if name and name not in seen:
                artists.append(name)
                seen.add(name)
    return artists
