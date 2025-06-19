from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_image_by_name(auto_name):
    url = "https://yandex.ru/images"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    search_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[@class='HeaderForm-Input mini-suggest__input']")))

    search_box.send_keys(auto_name)
    search_box.send_keys(Keys.ENTER)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    print(driver.current_url)
    driver.quit()

    img = soup.find("img", attrs={"class": "ImagesContentImage-Image"})
    link = img.get("src")
    if link and not link.startswith("http"):
        link = "https:" + link
    print(link)
    return link
