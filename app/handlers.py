from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery

import app.keyboards as kb
import app.database.requests as rq
import os

# импортируй файл метод вставляй ниже (found_car_by_photo)
import AI.AISearch as ai

router = Router()
class Car:
    def __init__(self, auto_name):
        self.auto_name = auto_name

    # def __init__(self, auto_name, engine_capacity, engine_power, drive_type, body_type, price, mileage, url):
    #     self.auto_name = auto_name
    #     self.engine_capacity = engine_capacity
    #     self.engine_power = engine_power
    #     self.drive_type = drive_type
    #     self.body_type = body_type
    #     self.price = price
    #     self.mileage = mileage
    #     self.url = url

car = Car('auto_name')

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer_photo(photo=FSInputFile('image\picture.png'),
                               caption='Привет! Я могу определить марку и модель автомобиля по фото,'
                                        ' а также подобрать актуальные объявления по найденному автомобилю'
                                        '\n\nПросто отправь фото или введи название автомобиля',
                               reply_markup=kb.main)

@router.message(F.photo)
async def found_car_by_photo(message: Message):
    photo_id = message.photo[-1].file_id
    file = await message.bot.get_file(photo_id)
    photo_name = f"{photo_id}.jpg"
    download_direction = "image"
    download_path = os.path.join(download_direction, photo_name)
    await message.bot.download_file(file.file_path, download_path)

    # Сюда метод
    car = Car(ai.found_car_by_photo(photo_name))

    await message.answer_photo(photo=FSInputFile('image\picture.png'),
                               caption='Нашел похожий автомобиль\n\n\n'
                                       f'Это {car.auto_name}\n\n'
                                       f'Объем двигателя: {"engine_capacity"}\n'
                                       f'Мощность: {"engine_power"}\n'
                                       f'Привод: {"drive_type"}\n'
                                       f'Тип кузова: {"body_type"} \n\n'
                                       f'Средняя цена на рынке: {"price"}',
                               reply_markup=kb.main_inline_keyboard)

@router.message(F.text == 'Избранное📌')
async def favourites(message: Message):
    await message.answer(text='Ваши избранные объявления:',
                         reply_markup=await kb.items(message.from_user.id))

@router.message(F.text)
async def found_car_by_text(message: Message):
    await message.answer_photo(photo=FSInputFile('image\picture.png'),
                               caption='Нашел похожий автомобиль\n\n\n'
                                       f'Это {car.auto_name}\n\n'
                                       f'Объем двигателя: {"engine_capacity"}\n'
                                       f'Мощность: {"engine_power"}\n'
                                       f'Привод: {"drive_type"}\n'
                                       f'Тип кузова: {"body_type"} \n\n'
                                       f'Средняя цена на рынке: {"price"}',
                               reply_markup=kb.main_inline_keyboard)

@router.callback_query(F.data == 'favourite')
async def favourites(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(text='Ваши избранные объявления:',
                         reply_markup=await kb.items(callback.message.from_user.id))

@router.callback_query(F.data == 'ad')
async def found_ad(callback: CallbackQuery):
    await callback.answer('Поиск объявлений')
    await callback.message.answer_photo(photo=FSInputFile('image\picture.png'),
                                        caption=f'{car.auto_name}\n\n'
                                                f'Объем двигателя: {"engine_capacity"}\n'
                                                f'Мощность: {"engine_power"}\n'
                                                f'Привод: {"drive_type"}\n'
                                                f'Тип кузова: {"body_type"}\n'
                                                f'Пробег: {"mileage"}\n\n'
                                                f'Цена: {"price"}',
                                        reply_markup=await kb.found_More_Ad('https://auto.drom.ru'))

@router.callback_query(F.data.startswith('items_'))
async def get_favourite_ad(callback: CallbackQuery):
    await callback.message.answer_photo(photo=FSInputFile('image\picture.png'),
                                        caption=f'{car.auto_name}\n\n'
                                                f'Объем двигателя: {"engine_capacity"}\n'
                                                f'Мощность: {"engine_power"}\n'
                                                f'Привод: {"drive_type"}\n'
                                                f'Тип кузова: {"body_type"}\n'
                                                f'Пробег: {"mileage"}\n\n'
                                                f'Цена: {"price"}',
                                        reply_markup=await kb.get_url_select_auto(callback.data.split("_")[1]))

@router.callback_query(F.data == 'add_favourites')
async def add_favourites(callback: CallbackQuery):
    await callback.answer('Добавленно в избранное')
    await rq.add_item(callback.message.from_user.id, car.auto_name, 'https://auto.drom.ru')