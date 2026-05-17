import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.thaliahallchicago.com"


def get_artists() -> list[str]:
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
    for tag in soup.find_all("div", class_="title"):
        text = tag.get_text(strip=True)
        # Strip "with ...", featuring, collab markers, subtitles
        name = re.split(r"\s+(?:with|feat|featuring|&|\+|-|:|\()", text, flags=re.IGNORECASE)[0].strip()
        if name and name not in seen:
            artists.append(name)
            seen.add(name)
    return artists
