from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 1. Настраиваем Selenium (используем Chrome)
driver = webdriver.Chrome()  # Убедитесь, что ChromeDriver установлен

# 2. Открываем сайт
driver.get("https://www.youtube.com")

# 3. Находим поисковую строку и вводим запрос
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys("Python разработка")
search_box.send_keys(Keys.ENTER)  # Эмулируем нажатие Enter

# 4. Ждем загрузки результатов (можно заменить на явное ожидание)
time.sleep(3)

# 5. Получаем все ссылки на видео
videos = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
print("Найденные видео:")
for i, video in enumerate(videos[:5], 1):
    print(f"{i}. {video.get_attribute('href')}")

# 6. Закрываем браузер
driver.quit()