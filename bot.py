from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
import emoji

negan1 = 'negan1.jpeg'
negan2 = 'negan2'
negan3 = 'negan3'
negan4 = 'negan4'



bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Hello! \nWrite something to me!')

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Write something to me and I will answer with the same text!')

@dp.message(commands=['voice'])
async def process_start_command(message: types.Message):
    await bot.send_voice(message.from_user.id, negan1, reply_to_message_id=message.message_id)

@dp.message()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)






