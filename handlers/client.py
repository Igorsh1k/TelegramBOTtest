from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from aiogram.dispatcher.filters import Text

cart = {}

async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Привіт вас вітає магазин комп'ютерної переферії 'ProGames'", reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply("Розмова з ботом через особисті повідомлення, напишіть боту:\nhttps://t.me/weathergoodbrobot")

async def ProGames_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Понеділок-Пятниця з 9:00 до 20:00, Субота-Неділя з 10:00 по 19:00')

async def ProGames_good_command(message: types.Message):
    urlkb = InlineKeyboardMarkup(row_width=2)
    urlButton = InlineKeyboardButton(text='Відвідайте наш ютуб канал', url='https://www.youtube.com/')
    urlButton2 = InlineKeyboardButton(text='Наш сайт', url='http://google.com/')
    x = [
        InlineKeyboardButton(text='Інстаграм', url='https://www.instagram.com/shurgaluyk/'),
        InlineKeyboardButton(text='Фейсбук', url='https://www.facebook.com/profile.php?id=100042418190508'),
        InlineKeyboardButton(text='Твітер', url='https://twitter.com/IgorSurgalyuk')
    ]
    urlkb.add(urlButton, urlButton2).row(*x).insert(InlineKeyboardButton(text='Наш сайт', url='http://google.com/'))
    await bot.send_message(message.from_user.id, "Ось декілька посилань:", reply_markup=urlkb)

async def ProGames_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Татарів вул.Незалежності')

@dp.message_handler(commands=['Меню'])
async def ProGames_menu_command(message: types.Message):
    items = await sqlite_db.sql_read2()
    for ret in items:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(f'{ret[1]} - {ret[-1]}', callback_data=f'add_to_cart_{ret[1]}'))
        keyboard.add(InlineKeyboardButton('Додати до корзини', callback_data=f'add_to_cart_{ret[1]}'))
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОпис: {ret[2]}\nЦіна {ret[-1]}', reply_markup=keyboard)

view_cart_button = types.KeyboardButton('/Корзина')

async def view_cart(message: types.Message):
    purchases = await sqlite_db.sql_read_purchases()
    if purchases:
        for purchase in purchases:
            item_text = f"Назва: {purchase[1]}\nОпис: {purchase[2]}\nЦіна: {purchase[3]}\n" \
                        f"Кількість: {purchase[4]}\nЗагальна вартість: {purchase[5]}"
            keyboard = create_cart_buttons(purchase[1])
            keyboard.add(InlineKeyboardButton("Видалити всі товари", callback_data="delete_all_items"))
            await bot.send_message(message.from_user.id, item_text, reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id, "Корзина порожня")

def create_cart_buttons(product_name):
    delete_button = InlineKeyboardButton("Видалити", callback_data=f"delete_from_cart_{product_name}")
    edit_button = InlineKeyboardButton("Редагувати", callback_data=f"edit_cart_{product_name}")
    keyboard = InlineKeyboardMarkup().add(delete_button, edit_button)
    return keyboard

async def voting_command(message: types.Message):
    vote_button = InlineKeyboardButton(text='Голосування', callback_data='vote')
    inkb = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='Like', callback_data='like_1'),
        InlineKeyboardButton(text='Dis Like', callback_data='like_-1'),
        vote_button
    )
    await message.answer('За те чи подобається вам телеграм бот', reply_markup=inkb)

answ = dict()
inkb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Like', callback_data='like_1'),
    InlineKeyboardButton(text='Dis Like', callback_data='like_-1'),
    InlineKeyboardButton(text='Голосування', callback_data='vote')
)

@dp.callback_query_handler(Text(startswith='like_'))
async def www_call(callback: types.CallbackQuery):
    res = int(callback.data.split('_')[1])
    if f'{callback.from_user.id}' not in answ:
        answ[f'{callback.from_user.id}'] = res
        await callback.answer('Ви проголосували')
    else:
        await callback.answer('Ви вже проголосували', show_alert=True)

@dp.callback_query_handler(Text(equals='vote'))
async def vote_call(callback: types.CallbackQuery):
    likes = sum(answ.values())
    await callback.answer(f'Загальна кількість голосів: {likes}')

@dp.callback_query_handler(Text(startswith='add_to_cart_'))
async def add_to_cart(callback: types.CallbackQuery):
    product_name = callback.data.split('_')[-1]
    added = await sqlite_db.sql_add_to_cart(product_name)
    if added:
        await callback.answer("Товар додано до корзини")
    else:
        await callback.answer("Помилка: товар не знайдено в меню", show_alert=True)

@dp.callback_query_handler(Text(startswith='delete_from_cart_'))
async def delete_from_cart(callback: types.CallbackQuery):
    product_name = callback.data.split('_')[-1]
    await sqlite_db.sql_delete_from_cart(product_name)
    await callback.answer("Товар видалено з корзини")

@dp.callback_query_handler(Text(equals='delete_all_items'))
async def delete_all_items(callback: types.CallbackQuery):
    await sqlite_db.sql_delete_all_items()
    await callback.answer("Усі товари видалено з корзини")

@dp.callback_query_handler(Text(startswith='edit_cart_'))
async def edit_cart_callback(callback: types.CallbackQuery):
    product_name = callback.data.split('_')[2]
    product = await sqlite_db.sql_get_product(product_name)
    if product:
        # Отримати деталі товару
        name = product[1]
        description = product[2]
        price = product[3]
        quantity = 1  # Початкова кількість товару

        # Створити кнопки для зміни кількості товару
        decrease_button = InlineKeyboardButton("➖", callback_data=f"decrease_quantity_{product_name}")
        increase_button = InlineKeyboardButton("➕", callback_data=f"increase_quantity_{product_name}")

        # Створити клавіатуру з кнопками зміни кількості товару
        quantity_keyboard = InlineKeyboardMarkup().add(decrease_button, increase_button)

        # Отримати загальну вартість товару
        total_price = float(price) * quantity

        # Створити повідомлення з деталями товару та кнопками зміни кількості
        message_text = f"Назва: {name}\nОпис: {description}\nЦіна: {price}\n" \
                       f"Кількість: {quantity}\nЗагальна вартість: {total_price}"
        await bot.send_message(callback.from_user.id, message_text, reply_markup=quantity_keyboard)
        await callback.answer()
    else:
        await callback.answer("Товар не знайдено", show_alert=True)

@dp.callback_query_handler(Text(startswith='increase_quantity_'))
async def increase_quantity_callback(callback: types.CallbackQuery):
    product_name = callback.data.split('_')[2]
    # Отримати поточну кількість товару
    current_quantity = await sqlite_db.sql_get_product_quantity(product_name)
    if current_quantity is not None:
        # Збільшити кількість товару
        new_quantity = current_quantity + 1
        await sqlite_db.sql_update_product_quantity(product_name, new_quantity)
        await callback.answer(f"Кількість товару збільшено: {new_quantity}")
    else:
        await callback.answer("Товар не знайдено", show_alert=True)

@dp.callback_query_handler(Text(startswith='decrease_quantity_'))
async def decrease_quantity_callback(callback: types.CallbackQuery):
    product_name = callback.data.split('_')[2]
    # Отримати поточну кількість товару
    current_quantity = await sqlite_db.sql_get_product_quantity(product_name)
    if current_quantity is not None and current_quantity > 1:
        # Зменшити кількість товару
        new_quantity = current_quantity - 1
        await sqlite_db.sql_update_product_quantity(product_name, new_quantity)
        await callback.answer(f"Кількість товару зменшено: {new_quantity}")
    else:
        await callback.answer("Неможливо зменшити кількість товару", show_alert=True)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(ProGames_open_command, commands=['Режим_роботи'])
    dp.register_message_handler(ProGames_place_command, commands=['Адреса'])
    dp.register_message_handler(ProGames_menu_command, commands=['Меню'])
    dp.register_message_handler(ProGames_good_command, commands=['Посилання'])
    dp.register_message_handler(voting_command, commands=['Голосування'])
    dp.register_message_handler(view_cart, commands=['Корзина'])
    kb_client.add(view_cart_button)

    dp.register_callback_query_handler(edit_cart_callback, Text(startswith='edit_cart_'))
    dp.register_callback_query_handler(increase_quantity_callback, Text(startswith='increase_quantity_'))
    dp.register_callback_query_handler(decrease_quantity_callback, Text(startswith='decrease_quantity_'))
