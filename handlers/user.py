from aiogram.types import LabeledPrice, Message, PreCheckoutQuery, ContentType
from aiogram.dispatcher.filters import Command
import create_bot
from create_bot import bot, dp
from create_bot import PAYTOKEN

price= [LabeledPrice(label='Notebook', amount=500000)]

@dp.message_handler(Command('start'))
async def start(message: Message):
    await bot.send_message(message.chat.id, 'Вітаєм!')

@dp.message_handler(Command('buy'))
async def buy_process(messasge: Message):
    await bot.send_invoice(messasge.chat.id,
                           title='Laptop',
                           description='Description',
                           provider_token = create_bot.PAYTOKEN,
                           currency='uan',
                           need_email=True,
                           prices=price,
                           start_parameter='exemple',
                           payload='some_invoice')

@dp.pre_checkout_querry_handler(lambda query: True)
async def pre_checkout_process(pre_checkout: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await bot.send_message(message.chat.id, 'Оплата пройшла успішно!')










@dp.message_handler(commands=['add_to_cart'])
async def add_to_cart_command(message: types.Message):
    user_id = message.from_user.id
    product_name = message.text.split()[1]
    quantity = int(message.text.split()[2])
    purchase_id = await sqlite_db.sql_add_purchase(user_id, product_name, "", "", quantity, "")
    await bot.send_message(message.from_user.id, f'{quantity}x {product_name} додано до корзини. Покупка_ID: {purchase_id}')

@dp.message_handler(commands=['view_cart'])
async def view_cart_command(message: types.Message):
    purchases = await sqlite_db.sql_read_purchases()
    if purchases:
        for purchase in purchases:
            purchase_id = purchase[0]
            product_name = purchase[1]
            quantity = purchase[4]
            total_price = purchase[5]
            await bot.send_message(
                message.from_user.id, f'{product_name} ({quantity} шт.) - {total_price} грн'
            )
    else:
        await bot.send_message(message.from_user.id, 'Корзина порожня')

@dp.message_handler(commands=['remove_from_cart'])
async def remove_from_cart_command(message: types.Message):
    product_name = message.text.split()[1]
    await sqlite_db.sql_delete_purchase_by_product_name(product_name)
    await bot.send_message(message.from_user.id, f'Товар "{product_name}" видалено з корзини')
