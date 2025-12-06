import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ------------------------
# INPUT
# ------------------------
# On Apify, you can pass input JSON when starting the actor
# Example input:
# {
#     "search_query": "resort in Siargao",
#     "max_scrolls": 12
# }
import sys
input_data = {}
if sys.stdin.isatty():
    # running locally, fallback
    input_data = {"search_query": "resort in Siargao", "max_scrolls": 12}
else:
    input_data = json.load(sys.stdin)

search_query = input_data.get("search_query", "resort in Siargao")
max_scrolls = input_data.get("max_scrolls", 12)

# ------------------------
# SETUP CHROME
# ------------------------
options = Options()
options.add_argument("--headless=new")  # headless mode for Apify
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}")
time.sleep(5)

# Wait for results
scroll_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
)

# Scroll to load more results
for _ in range(max_scrolls):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
    time.sleep(1.5)

# Extract listings
places = driver.find_elements(By.XPATH, '//div[@role="article"]')
data = []

for index, place in enumerate(places):
    try:
        name = place.find_element(By.XPATH, './/div[contains(@class,"fontHeadlineSmall")]').text
    except:
        name = ""
    try:
        address = place.find_element(By.XPATH, './/div[contains(@class,"Io6YTe")][2]').text
    except:
        address = ""
    try:
        rating = place.find_element(By.XPATH, './/span[contains(@aria-label,"stars")]').text
    except:
        rating = ""
    try:
        reviews = place.find_element(By.XPATH, './/span[contains(@aria-label,"reviews")]').text
    except:
        reviews = ""

    # Open the place in a new tab to get website, phone, email
    try:
        link = place.find_element(By.TAG_NAME, "a").get_attribute("href")
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)

        try:
            website = driver.find_element(By.XPATH, '//a[contains(@aria-label,"Website")]').get_attribute("href")
        except:
            website = ""

        try:
            phone = driver.find_element(By.XPATH, '//button[contains(@aria-label,"Phone") or contains(@aria-label,"Call")]').text
        except:
            phone = ""

        try:
            email_element = driver.find_element(By.XPATH, '//a[contains(@href,"mailto:")]')
            email = email_element.get_attribute("href").replace("mailto:", "")
        except:
            email = ""

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        website = ""
        phone = ""
        email = ""

    data.append({
        "name": name,
        "address": address,
        "rating": rating,
        "reviews": reviews,
        "website": website,
        "email": email,
        "phone": phone
    })
    print(f"Scraped {index + 1}/{len(places)}: {name}")

driver.quit()

# ------------------------
# OUTPUT
# ------------------------
# On Apify, the actor output is written to stdout as JSON
print(json.dumps(data, indent=4))
