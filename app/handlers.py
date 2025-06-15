from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto

import app.keyboards as kb
import app.database.requests as rq
import app.parser.drom_parser as drom_prs
import app.parser.wiki_parser as wiki_prs
import os

import AI.AISearch as ai

router = Router()

searched_auto_ai = ""
searched_auto_wiki = ""
ads = []
index = 0
car = ''
page = 1

class Car:
    def __init__(self, info_dict: dict):
        self.auto_name = info_dict['auto_name']
        self.price = info_dict['price']
        self.engine = info_dict['engine']
        self.fuel = info_dict['fuel']
        self.gearbox = info_dict['gearbox']
        self.drive_type = info_dict['drive_type']
        self.mileage = info_dict['mileage']
        self.url = info_dict['url']
        self.photo = info_dict['photo']

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer_photo(photo=FSInputFile(r'image\picture.png'),
                               caption='Привет! Я могу определить марку и модель автомобиля по фото,'
                                        ' а также подобрать актуальные объявления по найденному автомобилю'
                                        '\n\nПросто отправь фото или введи название автомобиля',
                               reply_markup=kb.main)

@router.callback_query(F.data == 'main_menu')
async def favourites(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer_photo(photo=FSInputFile(r'image\picture.png'),
                               caption='Привет! Я могу определить марку и модель автомобиля по фото,'
                                       ' а также подобрать актуальные объявления по найденному автомобилю'
                                       '\n\nПросто отправь фото или введи название автомобиля',
                               reply_markup=kb.main)

@router.message(F.photo)
async def found_car_by_photo(message: Message):
    global searched_auto_ai, ads, index, car, page
    photo_id = message.photo[-1].file_id
    file = await message.bot.get_file(photo_id)
    photo_name = f"{photo_id}.jpg"
    download_direction = "image"
    download_path = os.path.join(download_direction, photo_name)
    await message.bot.download_file(file.file_path, download_path)

    searched_auto_ai = ai.found_car_by_photo(photo_name)
    ads = []
    index = 0
    car = ''
    page = 1
    info = wiki_prs.get_car_info(searched_auto_ai)
    if (type(info) == str):
        await message.answer(text=info, reply_markup=kb.main)
    else:
        media = []
        for img in info['car_images']:
            media.append(InputMediaPhoto(type='photo', media=img))
        await message.answer_media_group(media)
        await message.answer(text='Нашел похожий автомобиль\n\n'
                                  f'Это {searched_auto_ai}\n\n'
                                  f'{info["car_info"]}',
                             reply_markup=kb.get_main_inline_keyboard(info['url']))

@router.message(F.text == 'Избранное📌')
async def favourites(message: Message):
    await message.answer(text='(BETA)Ваши избранные объявления:',
                         reply_markup=await kb.items(message.from_user.id))

@router.message(F.text)
async def found_car_by_text(message: Message):
    global searched_auto_wiki
    info = wiki_prs.get_car_info(message.text)
    if (type(info) == str):
        await message.answer(text=info, reply_markup=kb.main)
    else:
        media = []
        for img in info['car_images']:
                media.append(InputMediaPhoto(type='photo', media=img))
        searched_auto_wiki = info['car_name']
        await message.answer_media_group(media)
        await message.answer(text='Нашел похожий автомобиль\n\n'
                                  f'Это {info["car_name"]}\n\n'
                                  f'{info["car_info"]}',
                             reply_markup=kb.get_main_inline_keyboard(info['url']))

@router.callback_query(F.data == 'favourite')
async def favourites(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(text='(BETA)Ваши избранные объявления:',
                         reply_markup=await kb.items(callback.message.from_user.id))

@router.callback_query(F.data == 'ad')
async def found_ad(callback: CallbackQuery):
    global ads, index, car, searched_auto_ai, page
    await callback.answer('Поиск объявлений')
    if len(ads) == 0:
        if searched_auto_ai != '':
            name = searched_auto_ai.lower().split()
            del name[-2]
            name = ' '.join(name)
        elif searched_auto_wiki != '':
            name = searched_auto_wiki
        ads = drom_prs.get_drom_ads_with_photos(name)
        index = 0
    elif index >= len(ads):
        page += 1
        ads = drom_prs.get_more_drom_ads_(page)
        index = 0
    car = Car(ads[index])
    index += 1
    await callback.message.answer_photo(photo=car.photo,
                                        caption=f'{car.auto_name}\n\n'
                                                f'Двигатель: {car.engine}\n'
                                                f'Топливо: {car.fuel}\n'
                                                f'Привод: {car.drive_type}\n'
                                                f'КПП: {car.gearbox}\n'
                                                f'Пробег: {car.mileage}\n\n'
                                                f'Цена: {car.price}',
                                        reply_markup=await kb.found_More_Ad(car.url))

@router.callback_query(F.data.startswith('items_'))
async def get_favourite_ad(callback: CallbackQuery):
    await callback.message.answer_photo(photo=FSInputFile(r'image\picture.png'),
                                        caption=f'(BETA){car.auto_name}\n\n'
                                                f'Объем двигателя: {"engine_capacity"}\n'
                                                f'Мощность: {"engine_power"}\n'
                                                f'Привод: {"drive_type"}\n'
                                                f'Тип кузова: {"body_type"}\n'
                                                f'Пробег: {"mileage"}\n\n'
                                                f'Цена: {"price"}',
                                        reply_markup=await kb.get_url_select_auto(callback.data.split("_")[1]))

@router.callback_query(F.data == 'add_favourites')
async def add_favourites(callback: CallbackQuery):
    global car
    await callback.answer('(BETA)Добавленно в избранное')
    await rq.add_item(callback.message.from_user.id, car.auto_name, car.url)