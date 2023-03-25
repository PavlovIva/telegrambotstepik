from aiogram import Bot, Dispatcher, types
from config import TOKEN
import random
from aiogram.filters import Text, Command




bot = Bot(token=TOKEN)
dp = Dispatcher()
ATTEMPTS = 7
user: dict = {
    'in_game': False,
    'secret_number': None,
    'attempts': None,
    'total_games': 0,
    'wins': 0
}
def get_random_number() -> int:
    return random.randint(1, 100)



@dp.message(Command(commands=['start'])) # Реакция на комманду start
async def process_start(message: types.Message):
    await message.reply('Привет! Сыграем в "Угадай число?(Да/Нет) Подробные правила по команде /help')



@dp.message(Command(commands=['help']))  # Реакция на комманду help
async def help_process(message: types.Message):
    await message.reply('1) Число от 1 до 100. Если неверно - сообщу, меньше или больше\n2)Количество попыток: 3\n'
                        '3) Возможные комманды: /start, /help, /cansel, /stat\n4) Если игра идет, можно отправить только числа в пределах 1-100')


@dp.message(Command(commands=['stat']))  # Статистка игрока
async def show_stat(message: types.Message):
    await message.reply(f'Total games: {user["total_games"]}\n'
                        f'Total wins: {user["wins"]}')



@dp.message(Command(commands=['cansel']))  # Выход из игры
async def cancel_game(message: types.Message):
    if user['in_game']:
        await message.answer('Вы вышли из игры. Напишите нам, если хотите сыграть еще раз.')
        user['in_game'] = False
    else:
        await message.answer('А мы и так с вами играем.'
                             "Может сыграем разок?")




@dp.message(Text(text=["да", "игра", "сыграем", "давай", "хочу играть"], ignore_case=True))  # Запуск игры
async def some(message: types.Message):
    await message.answer("Хорошо! Число загадано!")
    user['secret_number'] = get_random_number()
    user['attempts'] = ATTEMPTS
    user['in_game'] = True


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def process_negative_answer(message: types.Message):
    if not user['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, числа от 1 до 100')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: types.Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            await message.answer('Ура!!! Вы угадали число!\n\n'
                                 'Может, сыграем еще?')
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
        elif int(message.text) > user['secret_number']:
            await message.answer('Мое число меньше')
            user['attempts'] -= 1
        elif int(message.text) < user['secret_number']:
            await message.answer('Мое число больше')
            user['attempts'] -= 1

        if user['attempts'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось '
                                 f'попыток. Вы проиграли :(\n\nМое число '
                                 f'было {user["secret_number"]}\n\nДавайте '
                                 f'сыграем еще?')
            user['in_game'] = False
            user['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_text_answers(message: types.Message):
    if user['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')








if __name__ == '__main__':
    dp.run_polling(bot)
