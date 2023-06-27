from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



# Кнопки клавіатури для адміна
button_load = KeyboardButton('/Загрузити')
button_delete = KeyboardButton('/Видалити')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load)\
    .add(button_delete)