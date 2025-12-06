import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ----- Setup Chrome -----
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

search_query = "resort in siargao"
driver.get(f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}")
time.sleep(5)

# Wait for the results sidebar
scroll_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
)

# Scroll to load more results
for _ in range(12):
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

    # Open the place details in a new tab to get website & email
    try:
        link = place.find_element(By.TAG_NAME, "a").get_attribute("href")
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)  # wait for page to load

        try:
            website = driver.find_element(By.XPATH, '//a[contains(@aria-label,"Website")]').get_attribute("href")
        except:
            website = ""

        # Try to find email on the page (some business pages show email in text)
        try:
            email_element = driver.find_element(By.XPATH, '//a[contains(@href,"mailto:")]')
            email = email_element.get_attribute("href").replace("mailto:", "")
        except:
            email = ""
        try:
            phone = driver.find_element(By.XPATH, '//button[contains(@aria-label,"Phone") or contains(@aria-label,"Call")]').text
        except:
            phone = ""
            
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        website = ""
        email = ""
        phone = ""

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

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("google_maps_leads_full.csv", index=False)
print(f"Saved {len(data)} leads to google_maps_leads_full.csv")

driver.quit()
