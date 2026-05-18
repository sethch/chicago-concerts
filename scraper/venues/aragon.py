import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.aragonballroomchicago.com/shows"


def get_artists() -> list[dict]:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "chakra-linkbox__overlay"))
        )
    except Exception:
        pass

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    artists = []
    seen = set()
    for a in soup.find_all("a", class_="chakra-linkbox__overlay"):
        text = a.get_text(strip=True)
        show_url = a.get("href", "")
        name = text.split(":")[0].strip()
        name = re.split(r"\s+(?:with|feat|featuring|&|\+|w/)", name, flags=re.IGNORECASE)[0].strip()
        name = re.split(r"\s*[–-]\s+", name)[0].strip()
        if name and name not in seen:
            artists.append({"name": name, "show_url": show_url})
            seen.add(name)
    return artists
