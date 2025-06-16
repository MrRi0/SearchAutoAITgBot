import wikipedia
import re

wikipedia.set_lang('ru')

def get_car_info(car_name):
    try:
        page = wikipedia.page(car_name)
        car_info = page.summary

        if not car_info_check(car_info):
            return 'Ошибка. Не могу найти данный автомобиль. Введите название по-другому. Или это не автомобиль'

        car_name = page.title
        car_imgs = [i for i in page.images if i[-3:] != 'svg'][:3]
        url = page.url
        return {"car_name" : car_name,
                "car_info" : car_info,
                "car_images" : car_imgs,
                "url" : url}
    except:
        return 'Ошибка. Не могу найти данный автомобиль. Введите название по-другому'

def car_info_check(car_info : str):
    info = set(re.split(r'[—:;!,.\n? ]+', car_info.lower()))

    if len(info) == 0: return False

    key_words = ('автомобиль автомобилей автомобиля автомобилю автомобилем'
                 'автомобиле машина авто спорткар маслкар суперкар'
                 'родстер купе хетчбэк пикап кроссовер джип '
                 'внедорожник седан лифтбэк лимузин минивэн '
                 'хардтоп таун-кар комби фастбек фаэтон ландо '
                 'тарга кабриолет спайдер спидстер торпедо баркетта'
                 'универсал фургон брогам ландо тарга').split()

    for key_word in key_words:
        if key_word in info:
            return True

    return False
