import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.thaliahallchicago.com"


def get_artists() -> list[dict]:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
    except Exception:
        pass

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    artists = []
    seen = set()
    for card in soup.find_all("div", class_="eb-item"):
        title_div = card.find("div", class_="title")
        if not title_div:
            continue
        text = title_div.get_text(strip=True)
        name = re.split(r"\s+(?:with|feat|featuring|&|\+|-|:|\()", text, flags=re.IGNORECASE)[0].strip()
        name = re.sub(r"^\*?SOLD\s*OUT\*?\s*", "", name, flags=re.IGNORECASE).strip()

        show_url = ""
        for a in card.find_all("a", href=True):
            href = a.get("href", "")
            if "google.com/maps" not in href:
                show_url = href
                break

        if name and name not in seen:
            artists.append({"name": name, "show_url": show_url})
            seen.add(name)
    return artists
