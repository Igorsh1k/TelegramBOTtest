#import python_weather
from aiogram import  Bot, Dispatcher, executor, types

#bot init
bot = Bot(token="5778746136:AAFPbY1o6gaA9k1A7Wxw6p6NrIcH7-yHQHg")
dp = Dispatcher(bot)

#echo
@dp.message_handler()
async def echo(message: types.Message):


    await message.answer(message.text)

if __name__ =="__main__":
    executor.start_polling(dp, skip_updates = True)
