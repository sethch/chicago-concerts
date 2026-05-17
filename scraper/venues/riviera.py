import requests
from bs4 import BeautifulSoup

URL = "https://www.rivieratheatre.com/events"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_artists() -> list[str]:
    page = requests.get(URL, headers=HEADERS, verify=False)
    soup = BeautifulSoup(page.text, "html.parser")
    artists = []
    seen = set()
    for item in soup.find_all("div", class_="eventItem"):
        title = item.find("h3", class_="title")
        if title and title.a:
            name = title.a.text.strip()
            if name and name not in seen:
                artists.append(name)
                seen.add(name)
    return artists
