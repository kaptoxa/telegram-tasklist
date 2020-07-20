import exceptions
from tasklist import TaskListBot
from aiogram import types
from aiogram.dispatcher import FSMContext
from pprint import pprint
from misc import Phase

from misc import dp, get_jedy


@dp.message_handler(state=Phase.EDIT_TASK | Phase.EDIT_IDEA | Phase.EDIT_ARCH)
async def add_task(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    bot = get_jedy(chat_id)


    print('handler text phase editing!')
    data = await state.get_data()
    pprint(data['task'])

    """Добавляет описание задачи"""
    bot.update_task_description(data['task'].id, message.text)

    answer_message = (
        f"Описание задачи дополнено.\n")
    await message.answer(answer_message)

@dp.message_handler(state='*', content_types=types.ContentTypes.TEXT)
async def add_task(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    bot = get_jedy(chat_id)

    print('text handler!')
    cur_state = await state.get_state()
    pprint(cur_state)

    """Добавляет новую задачу"""
    task = bot.add(message.text)

    answer_message = (
        f"Задачу эту теперь легко сделать будет.\n")
    await message.answer(answer_message)
