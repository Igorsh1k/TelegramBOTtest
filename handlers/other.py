from aiogram import types, Dispatcher
import json, string
from create_bot import dp
from data_base import sqlite_db

@dp.callback_query_handler(lambda query: query.data.startswith('add_to_cart_'))
async def add_to_cart_callback(query: types.CallbackQuery):
    product_name = query.data.split('_')[3]
    success = await sqlite_db.sql_add_to_cart(product_name)
    if success:
        await query.answer('Товар додано до кошика')
    else:
        await query.answer('Помилка: Товар не знайдено')

    await query.message.delete()

#@dp.message_handler()
async def echo_send(message : types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open("Matu.json")))) != set():
        await message.reply('Мати заборонені')
        await message.delete()

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)
    dp.register_callback_query_handler(add_to_cart_callback)