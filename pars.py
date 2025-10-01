from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os, csv
import random
import time

def create_driver():
    chrome_version = random.randint(110, 140)
    windows_version = random.randint(10, 11)
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT {windows_version}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=opts)

number_of_pages = 2
all_links = set()

def get_all_links_on_page(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
    elements = driver.find_elements(By.TAG_NAME, 'a')
    return {
        el.get_attribute('href')
        .replace("/reviews", "")
        .replace("/prices", "")
        .replace("/create", "")
        for el in elements if el.get_attribute('href')
    }

for page in range(1, number_of_pages + 1):
    url = f"https://catalog.onliner.by/mobile?page={page}"
    driver = create_driver()
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 4))
        links = get_all_links_on_page(driver)
        all_links.update(links)
        print(f"[Страница {page}] Собрано ссылок: {len(links)}")
    except Exception as e:
        print(f"[Ошибка] Страница {page} не загружена: {e}")

pd.DataFrame(list(all_links), columns=["Link"]).to_csv("onliner_links.csv", index=False)

with open('clean_links.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    count = 0
    for link in all_links:
        if link.startswith("https://catalog.onliner.by/mobile/") and len(link.split("/")) > 4:
            writer.writerow([link])
            count += 1
    print(f"[Фильтрация] Сохранено карточек товаров: {count}")

if os.path.exists("onliner_links.csv"):
    os.remove("onliner_links.csv")

def log_technique(name, type, power):
    file_exists = os.path.isfile('log_technique.csv')
    with open('log_technique.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Number', 'Name', 'Type', 'Power'])
        row_count = sum(1 for _ in open('log_technique.csv', encoding='utf-8')) - 1
        writer.writerow([row_count + 1, name, type, power])
