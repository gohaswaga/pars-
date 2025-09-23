from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os, csv

driver = webdriver.Chrome()

driver.get("https://catalog.onliner.by/mobile")

def get_all_links_on_page():
    elements = driver.find_elements(By.TAG_NAME, 'a') 
    ads_list = [element.get_attribute('href') for element in elements if element.get_attribute('href')]
    return ads_list

links = get_all_links_on_page()
df = pd.DataFrame(links, columns=["Links"])
df.to_csv("onliner_links.csv", index=False, encoding='utf-8')

driver.quit()

def log_technique(name, type, power):
    file_exists = os.path.isfile('log_technique.csv')
    
    with open('log_technique.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(['Number', 'Name', 'Type', 'Power'])
        
        
        if file_exists:
            with open('log_technique.csv', 'r', encoding='utf-8') as f:
                row_count = sum(1 for row in f) - 1
        else:
            row_count = 0
        
        writer.writerow([row_count + 1, name, type, power])
