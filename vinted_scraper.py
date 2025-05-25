from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to your chromedriver.exe — update if different
chromedriver_path = r'C:\Users\hanan\Desktop\chromedriver.exe'

service = Service(chromedriver_path)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Runs Chrome in background (no window)
options.add_argument('--disable-gpu')  # Recommended with headless

driver = webdriver.Chrome(service=service, options=options)

try:
    url = "https://www.vinted.co.uk/catalog?search_text=nike&price_to=100&order=newest_first&time=1748172368"
    driver.get(url)

    time.sleep(5)  # Wait for page to load fully (adjust if needed)

    items = driver.find_elements(By.CLASS_NAME, 'feed-grid__item')
    print(f"Found {len(items)} items")

    for item in items:
        try:
            title = item.find_element(By.CLASS_NAME, 'ItemPreview_title__').text
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            price = item.find_element(By.CLASS_NAME, 'Price_amount__').text
            print(f"{title} - {price}\n{link}\n")
        except Exception as e:
            print("Error extracting info from an item:", e)

finally:
    driver.quit()
