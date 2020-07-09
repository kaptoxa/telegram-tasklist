import exceptions
from keyboards import get_keyboard
from aiogram import types
from tasklist import TaskListBot
from pprint import pprint

from misc import dp, get_jedy


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Со cписком задач тебе Йода поможет.\n\n"
        "Задачу добавить: купить хлеба\n"
        "Cписок вывести: /list\n"
        "Обзор провести: /review\n")
        #"Кто вы узнать: /whoiam\n",
#        "Советы слушать: /hints")


@dp.message_handler(commands=['list'])
async def full_task_list(message: types.Message):
    chat_id = message.from_user.id
    bot = get_jedy(chat_id)

    """Отправляет весь список задач"""
    full_list = bot.all()
    if not full_list:
        await message.answer("Туманным будущее ваше является.")
        return

    to_post = [(i.id, i.text) for i in full_list]
    await message.answer('Задачи ваши Вам делать.', reply_markup=get_keyboard(to_post))


