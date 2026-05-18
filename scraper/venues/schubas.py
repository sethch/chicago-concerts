import requests
from bs4 import BeautifulSoup

URL = "https://www.lh-st.com/shows/"
HEADERS = {"User-Agent": "Mozilla/5.0"}


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
            if name and name not in seen:
                artists.append({"name": name, "show_url": show_url})
                seen.add(name)
    return artists
