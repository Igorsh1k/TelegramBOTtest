from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

b1 = KeyboardButton('/Режим_роботи')
b2 = KeyboardButton('/Адреса')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('/Посилання')
b5 = KeyboardButton('/Голосування')
b6 = KeyboardButton('/Корзина')  # Додано кнопку для перегляду корзини
#b4 = KeyboardButton('/Поділитись номером', request_contact=True)
#b5 = KeyboardButton('/Відправити де я',request_location=True)
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b3).add(b2).insert(b1).row(b4).insert(b5)