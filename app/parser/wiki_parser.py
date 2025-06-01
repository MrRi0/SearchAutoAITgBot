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