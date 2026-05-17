import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saltshedchicago.com/home"


def get_artists() -> list[str]:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ve-events__card-title"))
        )
    except Exception:
        pass

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    artists = []
    seen = set()
    for tag in soup.find_all("h3", class_="ve-events__card-title"):
        text = tag.get_text(strip=True)
        # Strip "SOLD OUT-" prefix and tour names after " - "
        text = re.sub(r"^SOLD OUT[-\s]+", "", text, flags=re.IGNORECASE)
        name = text.split(" - ")[0].strip()
        # Strip "feat:", "with", etc.
        name = re.split(r"\s+(?:with|feat|featuring|&|\+|w/)", name, flags=re.IGNORECASE)[0].strip()
        if name and name not in seen:
            artists.append(name)
            seen.add(name)
    return artists
