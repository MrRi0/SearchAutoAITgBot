from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_items

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Избранное📌', callback_data='favourite')]
])

main_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти объявления', callback_data='ad')],
    [InlineKeyboardButton(text='Избранное📌', callback_data='favourite')]
])

async def get_url_select_auto(url):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перейти к объявлению', url=url)],
    [InlineKeyboardButton(text='Избранное📌', callback_data='favourite')]
    ])
    return keyboard

async def found_More_Ad(url):
    more_Ad = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перейти к объявлению', url=url)],
    [InlineKeyboardButton(text='Найти еще объявления', callback_data='ad')],
    [InlineKeyboardButton(text='Добавить в избранное📌', callback_data='add_favourites')],
    [InlineKeyboardButton(text='Избранное📌', callback_data='favourite')]
    ])
    return more_Ad

async def items(tg_id):
    all_items = await get_items(tg_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'items_{item.url}'))
    keyboard.add(InlineKeyboardButton(text='Избранное📌', callback_data='favourite'))
    return keyboard.adjust(1).as_markup()