import exceptions
from tasklist import TaskListBot

from keyboards import get_keyboard
from aiogram import types
from aiogram.dispatcher import FSMContext

from misc import dp, Phase, logger, get_jedy


@dp.message_handler(state='*', commands=['start', 'help'])
async def send_welcome(message: types.Message, state: FSMContext):
    """Отправляет приветственное сообщение и помощь по боту"""
    logger.debug(f"Send welcome handler text: {message.text} !")

    await get_jedy(message.from_user.id, state)

    await message.answer(
        "Со cписком задач тебе Йода поможет.\n\n"
        "Добавить задачу: просто наберите в чате 'купить хлеба'\n"
        "Вывести списки задач: /todo /ideas /archive\n"
        "Обзор провести: /review\n")
        #"Кто вы узнать: /whoiam\n",
#        "Советы слушать: /hints")


@dp.message_handler(state='*', commands=['todo', 'ideas', 'archive'])
async def full_task_list(message: types.Message, state: FSMContext):
    """Отправляет список задач/идей/выполненного"""
    logger.debug(f"Commands handler {message.text}")
    jbot = await get_jedy(message.from_user.id, state)

    stage = ['/ideas', '/todo', '/archive'].index(message.text)
    await state.set_state(Phase.get(stage))

    full_list = jbot.tasks_list(stage)
    if not full_list:
        empty_message = {0: "Нет идей? Хватит медитировать!", 1: "Список задач пуст", 2: "Архив пуст"}
        await message.answer(empty_message[stage])
        return

    to_post = [(i.id, i.text) for i in full_list]
    list_name = {0: "Список идей:", 1: "Список задач:", 2: "Архив:"}
    await message.answer(list_name[stage], reply_markup=get_keyboard(to_post))


