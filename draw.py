from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()

file = ['BQACAgIAAxkBAAMqY-5FNjV7ar2JV8PkEa3XRfXKEAEAAhQrAAIzbXFLUmdqfMeMRNEuBA', 'BQACAgIAAxkBAAM1Y-5QfdrsjmMykYvBz8OV1LTFdssAAlcrAAIzbXFLIKNhOIb0oGsuBA']


@dp.message(content_types=["document", "video", "audio", "conf"])
async def process_start_command(message):
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    print(document_id)  # Выводим file_id
    await bot.send_document(message.chat.id, document_id)  # Отправляем пользователю file_id





@dp.message_handler(commands=['file'])
async def process_start_command(message):
    await bot.send_document(message.chat.id, file[1])





if __name__ == '__main__':
    executor.start_polling(dp)