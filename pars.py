from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import random
import time

def get_number_of_pages():
    while True:
        try:
            return int(input("Введите количество страниц для сканирования: "))
        except ValueError:
            print("Пожалуйста, введите целое число.")

def create_driver():
    chrome_version = random.randint(110, 140)
    windows_version = random.choice([10, 11])
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT {windows_version}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def get_links_from_page(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        elements = driver.find_elements(By.TAG_NAME, 'a')
        links = {
            el.get_attribute('href')
            .replace("/reviews", "")
            .replace("/prices", "")
            .replace("/create", "")
            for el in elements if el.get_attribute('href')
        }
        return links
    except Exception as e:
        print(f"[Ошибка] Не удалось загрузить {url}: {e}")
        return set()

def filter_product_links(links):
    return [
        link for link in links
        if link.startswith("https://catalog.onliner.by/mobile/") and len(link.split("/")) > 4
    ]

def save_links_to_csv(filename, links):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for link in links:
            writer.writerow([link])
    print(f"[Сохранение] Ссылки сохранены в файл: {filename}")

def collect_links():
    number_of_pages = get_number_of_pages()
    all_links = set()

    for page in range(1, number_of_pages + 1):
        url = f"https://catalog.onliner.by/mobile?page={page}"
        driver = create_driver()
        print(f"[Загрузка] Страница {page}: {url}")
        page_links = get_links_from_page(driver, url)
        all_links.update(page_links)
        print(f"[Сбор] Найдено ссылок: {len(page_links)}")
        driver.quit()
        time.sleep(random.uniform(1.5, 3.5))

    filtered_links = filter_product_links(all_links)
    save_links_to_csv("clean_links.csv", filtered_links)
    print(f"[Фильтрация] Сохранено карточек товаров: {len(filtered_links)}")

def get_characteristics():
    if not os.path.exists("clean_links.csv"):
        print("[Ошибка] Файл 'clean_links.csv' не найден.")
        return

    with open("clean_links.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        links = [row[0] for row in reader if row]

    driver = create_driver()

    with open("log_technique.csv", 'w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(['Number', 'Name', 'Price', 'Power', 'Link']) 

        for idx, link in enumerate(links, start=1):
            try:
                driver.get(link)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1')))

                
                try:
                    name = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/div[6]/div[2]/div/table/tbody[15]/tr[2]/td[2]/span').text
                except:
                    name = 'N/A'
                try:
                    price = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/div[1]/div[2]/div[5]/div[1]/div/a').text
                except:
                    price = 'N/A'
                try:
                    power = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/div[6]/div[2]/div/table/tbody[13]/tr[3]/td[2]/span').text
                except:
                    power = 'N/A'

                writer.writerow([idx, name, price, power, link])
                print(f"[{idx}/{len(links)}] Успешно: {link}")
            except Exception as e:
                print(f"[{idx}/{len(links)}] Ошибка: {link} — {e.__class__.__name__}")
            time.sleep(random.uniform(1.5, 3.0))

    driver.quit()
    print("[Готово] Данные сохранены в log_technique.csv")

if __name__ == "__main__":
    collect_links()
    get_characteristics()
