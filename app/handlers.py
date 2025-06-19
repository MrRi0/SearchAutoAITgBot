from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto

import app.keyboards as kb
import app.car_ad as car
import app.database.requests as rq
import app.parser.drom_parser as drom_prs
import app.parser.wiki_parser as wiki_prs
import app.parser.image_parser as img_prs
import os

import AI.AISearch as ai

router = Router()

searched_auto_ai = ""
searched_auto_wiki = ""
ads = []
index = 0
car_ad = None
page = 1

current_favorite_ad_id = 0

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer_photo(photo=FSInputFile(r'image\main_image.png'),
                               caption='Привет! Я могу определить марку и модель автомобиля по фото,'
                                        ' а также подобрать актуальные объявления по найденному автомобилю'
                                        '\n\nПросто отправь фото или введи название автомобиля',
                               reply_markup=kb.main)

@router.callback_query(F.data == 'main_menu')
async def favourites(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer_photo(photo=FSInputFile(r'image\main_image.png'),
                               caption='Привет! Я могу определить марку и модель автомобиля по фото,'
                                       ' а также подобрать актуальные объявления по найденному автомобилю'
                                       '\n\nПросто отправь фото или введи название автомобиля',
                               reply_markup=kb.main)

@router.message(F.photo)
async def found_car_by_photo(message: Message):
    global searched_auto_ai, ads, index, car_ad, page
    photo_id = message.photo[-1].file_id
    file = await message.bot.get_file(photo_id)
    photo_name = f"{photo_id}.jpg"
    download_direction = "image"
    download_path = os.path.join(download_direction, photo_name)
    await message.bot.download_file(file.file_path, download_path)

    searched_auto_ai = ai.found_car_by_photo(photo_name)
    if searched_auto_ai == 'Неопределено':
        await message.answer(text='Ошибка. Не могу найти данный автомобиль. Или это не автомобиль')
        return

    ads = []
    index = 0
    car_ad = None
    page = 1
    info = wiki_prs.get_car_info(searched_auto_ai)
    img_link = img_prs.get_image_by_name(searched_auto_ai)
    if (type(info) == str):
        await message.answer_photo(photo=img_link, caption='Нашел похожий автомобиль\n\n'
                                  f'Это {searched_auto_ai}',
                             reply_markup=kb.get_main_inline_keyboard_without_info())
    else:
        await message.answer_photo(photo=img_link)
        await message.answer(text='Нашел похожий автомобиль\n\n'
                                  f'Это {searched_auto_ai}\n\n'
                                  f'{info["car_info"]}',
                             reply_markup=kb.get_main_inline_keyboard(info['url']))

@router.message(F.text == 'Избранное📌')
async def favourites(message: Message):
    await message.answer(text='Ваши избранные объявления:',
                         reply_markup=await kb.items(message.from_user.id))

@router.message(F.text)
async def found_car_by_text(message: Message):
    global searched_auto_wiki
    info = wiki_prs.get_car_info(message.text)
    if (type(info) == str):
        await message.answer(text=info, reply_markup=kb.main)
    else:
        img_link = img_prs.get_image_by_name(info['car_name'])
        searched_auto_wiki = info['car_name']
        await message.answer_photo(photo=img_link)
        await message.answer(text='Нашел похожий автомобиль\n\n'
                                   f'Это {info["car_name"]}\n\n'
                                   f'{info["car_info"]}',
                           reply_markup=kb.get_main_inline_keyboard(info['url']))

@router.callback_query(F.data == 'favourite')
async def favourites(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(text='Ваши избранные объявления:',
                         reply_markup=await kb.items(callback.message.from_user.id))

@router.callback_query(F.data == 'ad')
async def found_ad(callback: CallbackQuery):
    global ads, index, car_ad, searched_auto_ai, page
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
    car_ad = ads[index]
    index += 1
    await callback.message.answer_photo(photo=car_ad.photo,
                                        caption=f'{car_ad.auto_name}\n\n'
                                                f'Двигатель: {car_ad.engine}\n'
                                                f'Топливо: {car_ad.fuel}\n'
                                                f'Привод: {car_ad.drive_type}\n'
                                                f'КПП: {car_ad.gearbox}\n'
                                                f'Пробег: {car_ad.mileage}\n\n'
                                                f'Цена: {car_ad.price}',
                                        reply_markup=await kb.found_More_Ad(car_ad.url))

@router.callback_query(F.data.startswith('items_'))
async def get_favourite_ad(callback: CallbackQuery):
    global current_favorite_ad_id
    favourite_ad = await rq.get_item(int(callback.data.split("_")[1]))
    current_favorite_ad_id = favourite_ad.id
    await callback.answer('')
    await callback.message.answer_photo(photo=favourite_ad.photo_url,
                                        caption=f'{favourite_ad.name}\n\n'
                                                f'Двигатель: {favourite_ad.engine}\n'
                                                f'Топливо: {favourite_ad.fuel}\n'
                                                f'Привод: {favourite_ad.drive_type}\n'
                                                f'КПП: {favourite_ad.gearbox}\n'
                                                f'Пробег: {favourite_ad.mileage}\n\n'
                                                f'Цена: {favourite_ad.price}',
                                        reply_markup=await kb.get_url_select_auto(favourite_ad.url))

@router.callback_query(F.data == 'delete_favorite')
async def add_favourites(callback: CallbackQuery):
    await callback.answer('Удаление')
    if (current_favorite_ad_id == 0):
        await callback.message.answer(text='Ошибка не удалось удалить')
    else:
        await rq.delete_item(current_favorite_ad_id)

@router.callback_query(F.data == 'add_favourites')
async def add_favourites(callback: CallbackQuery):
    await callback.answer('Добавленно в избранное')
    await rq.add_item(callback.message.from_user.id, car_ad)