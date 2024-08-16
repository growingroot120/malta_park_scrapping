import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os

# Read the CSV file
df = pd.read_csv('company_results.csv')

# Initialize the Selenium WebDriver (Chrome in this example)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Check if the file already exists
file_exists = os.path.isfile('info.csv')

# Prepare a list to store the extracted information
data = []

# Loop through each href link
for index, row in df.iterrows():
    url = row['Href']
    driver.get(url)

    # Initialize empty variables for each column
    name_text = ""
    price_text = ""
    tel_text = ""
    locality_text = ""
    category_text = ""
    
    try:
        name_element = driver.find_element(By.XPATH, '//h1')  # Adjust the XPath as needed
        name_text = name_element.text
        
        price_element = driver.find_element(By.CLASS_NAME, "top-price")
        price_text = price_element.text
        
        description_element = driver.find_element(By.CLASS_NAME, "readmore-wrapper")
        description_text = description_element.text
        
        # Find the 8-digit number using regular expression
        match = re.search(r'\b\d{8}\b', description_text)
        if match:
            tel_text = match.group()
        
        # Find all divs with class 'ui list fixed-label item-details'
        details_divs = driver.find_elements(By.CLASS_NAME, 'ui.list.fixed-label.item-details')
        
        for details_div in details_divs:
            # Find all spans with class 'item' inside the div
            item_spans = details_div.find_elements(By.CLASS_NAME, 'item')
            
            for item in item_spans:
                label_element = item.find_element(By.TAG_NAME, 'label')
                b_element = label_element.find_element(By.TAG_NAME, 'b')
                if b_element.text == 'Locality':
                    value_span = item.find_element(By.TAG_NAME, 'span')
                    locality_text = value_span.text
                if b_element.text == 'Category:':
                    category_text = item.text
        
        # Append the extracted information to the list
        data.append({
            'URL': url,  # Include URL to keep track of the source
            'Name': name_text,
            'Price': price_text,
            'Tel': tel_text,
            'Locality': locality_text,
            'Category': category_text
        })
        
        # Create a DataFrame from the extracted data
        df_info = pd.DataFrame(data)

        # Write the DataFrame to a CSV file
        if not file_exists:
            df_info.to_csv('info.csv', index=False)
            file_exists = True
        else:
            df_info.to_csv('info.csv', mode='a', header=False, index=False)
        
        # Clear the data list after writing to CSV
        data.clear()
        
        time.sleep(1)
    except Exception as e:
        print(f"Error for {url}: {e}")

# Close the driver
driver.quit()
