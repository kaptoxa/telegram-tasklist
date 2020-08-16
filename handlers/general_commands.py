import exceptions
from keyboards import get_keyboard
from aiogram import types
from aiogram.dispatcher import FSMContext
from tasklist import TaskListBot

from misc import dp, Phase, logger


@dp.message_handler(state='*', commands=['start', 'help'])
async def send_welcome(message: types.Message, state: FSMContext):
    """Отправляет приветственное сообщение и помощь по боту"""
    logger.info(f"Send welcome handler text: {message.text} !")

    await state.update_data(bot=TaskListBot(message.from_user.id))

    await state.set_state(Phase.TASKS)

    await message.answer(
        "Со cписком задач тебе Йода поможет.\n\n"
        "Добавить задачу: просто наберите в чате 'купить хлеба'\n"
        "Вывести списки задач: /todo /ideas /archive\n"
        "Обзор провести: /review\n")
        #"Кто вы узнать: /whoiam\n",
#        "Советы слушать: /hints")


@dp.message_handler(state='*', commands=['todo', 'ideas', 'archive'])
async def full_task_list(message: types.Message, state: FSMContext):
    logger.info(f"Commands handler {message.text}")
    data = await state.get_data()

    """Отправляет список задач"""
    stage = ['/ideas', '/todo', '/archive'].index(message.text)
    logger.info(f"stage = {stage}")

    await state.set_state(Phase.get(stage))

    cur_state = await state.get_state()
    logger.info(f"cur_state = {cur_state}")
    
    
    full_list = data['bot'].tasks_list(stage)
    if not full_list:
        empty_message = {0: "Нет идей? Хватит медитировать!", 1: "Список задач пуст", 2: "Архив пуст"}
        await message.answer(empty_message[stage])
        return

    to_post = [(i.id, i.text) for i in full_list]
    list_name = {0: "Список идей:", 1: "Список задач:", 2: "Архив:"}
    await message.answer(list_name[stage], reply_markup=get_keyboard(to_post))


