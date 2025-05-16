import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_drom_ads_with_photos(auto_name):
    url = "https://auto.drom.ru/"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-ftid='sales__filter_advanced-button']")))
    search_button.click()

    search_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[@data-ftid='sales__filter_keywords']")))
    search_box.send_keys(auto_name)
    search_box.send_keys(Keys.ENTER)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-ftid='bulls-list_bull']"))
    )

    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    ads = []
    blocks = soup.find_all("div", attrs={"data-ftid": "bulls-list_bull"})

    for idx, block in enumerate(blocks, start=1):
        try:
            # Название и ссылка
            title_tag = block.find("a", attrs={"data-ftid": "bull_title"})
            title = title_tag.get_text(strip=True) if title_tag else "—"
            link = title_tag.get("href") if title_tag else "—"
            if link and not link.startswith("http"):
                link = "https://auto.drom.ru" + link

            # Цена
            price_tag = block.find("span", attrs={"data-ftid": "bull_price"})
            price = price_tag.get_text(strip=True) if price_tag else "—"

            # Характеристики
            desc_block = block.find("div", attrs={"data-ftid": "component_inline-bull-description"})
            desc_items = []
            if desc_block:
                for span in desc_block.find_all("span"):
                    text = span.get_text(strip=True)
                    if text:
                        desc_items.append(text.replace(',', ''))

            img_tag = block.find("img", class_="css-9w7beg evrha4s0")
            img_url = img_tag["src"] if img_tag and "src" in img_tag.attrs else None

            ads.append({
                "auto_name": title,
                "price": price,
                "engine": desc_items[0],
                "fuel": desc_items[1],
                "gearbox": desc_items[2],
                "drive_type": desc_items[3],
                "mileage": desc_items[4],
                "url": link,
                "photo": img_url
            })
            print(ads)

        except Exception as e:
            print(f"⚠️ Ошибка при обработке объявления: {e}")
            continue

    return ads
