import exceptions
from tasklist import TaskListBot

from keyboards import get_keyboard
from aiogram import types
from aiogram.dispatcher import FSMContext

from misc import dp, Phase, logger, get_jedy, replicas


@dp.message_handler(state='*', commands=['start', 'help'])
async def send_welcome(message: types.Message, state: FSMContext):
    """Show hello message to help with bot"""
    logger.debug(f"Send welcome handler text: {message.text} !")

    await get_jedy(message.from_user.id, state)

    await message.answer(replicas['/help'])
#        "Со cписком задач тебе Йода поможет.\n\n"
#        "Добавить задачу: просто наберите в чате 'купить хлеба'\n"
#        "Вывести списки задач: /todo /ideas /archive\n"
#        "Обзор провести: /review\n")
        #"Кто вы узнать: /whoiam\n",
#        "Советы слушать: /hints")


@dp.message_handler(state='*', commands=['todo', 'ideas', 'archive'])
async def full_task_list(message: types.Message, state: FSMContext):
    """Show tasklist for a stage"""
    logger.debug(f"Commands handler {message.text}")
    jbot = await get_jedy(message.from_user.id, state)

    stage = ['/ideas', '/todo', '/archive'].index(message.text)
    await state.set_state(Phase.get(stage))

    full_list = jbot.tasks_list(stage)
    if not full_list:
        await message.answer(replicas['empty_list'][str(stage)])
        return

    to_post = [(i.id, i.text) for i in full_list]
    await message.answer(replicas['list'][str(stage)], reply_markup=get_keyboard(to_post))


