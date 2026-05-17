import requests
from bs4 import BeautifulSoup

URL = "https://www.subt.net"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_artists() -> list[str]:
    page = requests.get(URL, headers=HEADERS, verify=False)
    soup = BeautifulSoup(page.text, "html.parser")
    artists = []
    seen = set()
    for tag in soup.find_all("p", class_="headliners"):
        name = tag.text.strip()
        if name and name not in seen:
            artists.append(name)
            seen.add(name)
    return artists
