import re
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.emptybottle.com"


def get_artists() -> list[str]:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "performing"))
        )
    except Exception:
        pass

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    performances = []
    for card in soup.find_all("div", class_="eb-item"):
        date_div = card.find("div", class_="date")
        if not date_div:
            continue
        try:
            date_obj = datetime.strptime(date_div.text.strip(), "%a %B %d")
        except ValueError:
            continue

        performers = card.find("ul", class_="performing")
        if not performers:
            continue
        first = performers.find("li")
        if not first:
            continue

        name = first.text.strip()
        name = name.replace("*SOLD OUT* ", "").strip()
        name = name.split("-")[0].split("(")[0].split("with")[0].strip()
        name = re.sub(r"\s*(?:w|with|featuring|\+|&)\s.*$", "", name, flags=re.IGNORECASE)
        if name:
            performances.append((date_obj, name))

    performances.sort(key=lambda x: x[0])
    seen = set()
    artists = []
    for _, name in performances:
        if name not in seen:
            artists.append(name)
            seen.add(name)
    return artists
