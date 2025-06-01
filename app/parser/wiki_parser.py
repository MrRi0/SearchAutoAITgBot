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
import wikipedia

wikipedia.set_lang('ru')

def get_car_info(car_name):
    try:
        page = wikipedia.page(car_name)
        car_info = page.summary
        car_name = page.title
        car_imgs = [i for i in page.images if i[-3:] != 'svg'][:3]
        url = page.url
        return {"car_name" : car_name,
                "car_info" : car_info,
                "car_images" : car_imgs,
                "url" : url}
    except:
        print('Не могу найти автомобиль')
        return 'Ошибка. Не могу найти данный автомобиль. Введите название по-другому'