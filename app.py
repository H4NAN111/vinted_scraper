import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_vinted(max_price=25):
    st.write("Starting ChromeDriver...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/114.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    url = f"https://www.vinted.co.uk/catalog?price_to={max_price}&order=newest_first"
    st.write(f"Navigating to {url} ...")
    driver.get(url)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-grid__item")))

    products = []
    product_elements = driver.find_elements(By.CSS_SELECTOR, "div.feed-grid__item")
    st.write(f"Found {len(product_elements)} products on page.")

    for p in product_elements:
        try:
            link_elem = p.find_element(By.CSS_SELECTOR, "a")
            link = link_elem.get_attribute("href")
            title = link_elem.get_attribute("aria-label") or link_elem.text or "No title"

            try:
                price_elem = p.find_element(By.CSS_SELECTOR, "div.feed-price")
                price = price_elem.text.strip()
            except:
                price = "Price not found"

            products.append({"title": title.strip(), "link": link, "price": price})
        except Exception as e:
            st.write(f"Error scraping product: {e}")
            continue

    driver.quit()
    st.write("ChromeDriver closed.")
    return products

st.title("Vinted Monitoring Bot")

max_price = st.number_input("Max Price (£)", min_value=1, max_value=1000, value=25)

if st.button("Start Scraping"):
    st.write(f"Scraping products under £{max_price}...")
    products = scrape_vinted(max_price)

    if products:
        for p in products:
            st.markdown(f"**{p['title']}** - {p['price']}")
            st.markdown(f"[Link to product]({p['link']})")
    else:
        st.write("No products found.")
