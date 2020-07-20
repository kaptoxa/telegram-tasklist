import exceptions
from keyboards import get_keyboard
from aiogram import types
from aiogram.dispatcher import FSMContext
from tasklist import TaskListBot
from pprint import pprint

from misc import dp, get_jedy, Phase, logger


@dp.message_handler(state='*', commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    logger.info(f"Send welcome handler text: {message.text} !")
    await Phase.todo.set()

    await message.answer(
        "Со cписком задач тебе Йода поможет.\n\n"
        "Добавить задачу: купить хлеба\n"
        "Вывести списки задач: /todo /ideas /archive\n"
        "Обзор провести: /review\n")
        #"Кто вы узнать: /whoiam\n",
#        "Советы слушать: /hints")


@dp.message_handler(state='*', commands=['todo', 'ideas', 'archive'])
async def full_task_list(message: types.Message, state: FSMContext):
    logger.info(f"Commands handler {message.text}")
    chat_id = message.from_user.id
    bot = get_jedy(chat_id)

    """Отправляет список задач"""
    stage = ['/ideas', '/todo', '/archive'].index(message.text)

    await state.set_state(Phase.all()[stage])

    full_list = bot.tasks_list(stage)
    if not full_list:
        await message.answer("Туманным будущее ваше является.")
        return

    to_post = [(i.id, i.text) for i in full_list]
    await message.answer('Задачи ваши Вам делать.', reply_markup=get_keyboard(to_post))


