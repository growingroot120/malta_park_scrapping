import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Set Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode if needed
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-fullscreen")  # Open browser in full screen mode

# Initialize the WebDriver using webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to scrape a single page
def scrape_page(page_url):
    driver.get(page_url)
    # time.sleep(10)  # Allow some time for page to load completely
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "page-content-left")))
    # Close the "agree" button if it exists
    try:
        agree_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "closebutton")))
        agree_button.click()
    except:
        pass
    
    # Click the listings button if it exists
    try:
        listings_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "hopscotch-nav-button")))
        listings_button.click()
    except:
        pass
    
    content_divs = driver.find_elements(By.CLASS_NAME, "content")

    page_data = []
    for div in content_divs:
        try:
            link_element = div.find_element(By.TAG_NAME, "a")
            href = link_element.get_attribute("href")
            link_text = link_element.text
        except:
            href = "N/A"
            link_text = "N/A"
        
        try:
            price_element = div.find_element(By.CLASS_NAME, "price")
            price = price_element.text
        except:
            price = "N/A"

        page_data.append([link_text, href, price])

    return page_data

# Initialize the CSV file and write the header
with open("company_results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Link Text", "Href", "Price"])

try:
    # Scrape the first page
    first_page_url = "https://maltapark.com/listings/category/247"
    first_page_data = scrape_page(first_page_url)
    with open("company_results.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(first_page_data)
    print("Scraped first page")

    # Scrape subsequent pages from 2 to 88
    for page in range(2, 89):
        page_url = f"https://maltapark.com/listings/category/248/?page={page}&nr=4152&wr=53&bn=0"
        page_data = scrape_page(page_url)
        with open("company_resultslonglents.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(page_data)
        print(f"Scraped page {page}")

finally:
    # Close the WebDriver
    driver.quit()

print("Scraping completed. Results saved to company_results.csv")
