import requests
from bs4 import BeautifulSoup

URL = "https://www.subt.net"
HEADERS = {"User-Agent": "Mozilla/5.0"}


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
        if name and name not in seen:
            artists.append({"name": name, "show_url": show_url})
            seen.add(name)
    return artists
