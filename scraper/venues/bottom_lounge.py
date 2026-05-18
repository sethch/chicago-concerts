import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://bottomlounge.com/events/"


def get_artists() -> list[dict]:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    driver.get(URL)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "w-post-elm"))
        )
    except Exception:
        pass

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    artists = []
    seen = set()
    for art in soup.find_all("article"):
        h2 = art.find("h2", class_="w-post-elm")
        btn = art.find("a", class_="w-btn")
        if not h2:
            continue
        name = h2.get_text(strip=True)
        show_url = btn.get("href", "") if btn else ""
        name = name.split(",")[0].strip()
        name = re.split(r"\s+(?:with|feat|featuring|w/)", name, flags=re.IGNORECASE)[0].strip()
        name = re.split(r"\s*[–-]\s+", name)[0].strip()
        if name and name not in seen:
            artists.append({"name": name, "show_url": show_url})
            seen.add(name)
    return artists
