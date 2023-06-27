from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

TOKEN = "5778746136:AAFPbY1o6gaA9k1A7Wxw6p6NrIcH7-yHQHg"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

