import exceptions
from tasklist import TaskListBot
from aiogram import types
from aiogram.dispatcher import FSMContext

from misc import Phase, dp, logger, get_jedy


@dp.message_handler(state=Phase.EDIT_TASK | Phase.EDIT_IDEA | Phase.EDIT_ARCH)
async def add_task(message: types.Message, state: FSMContext):
    """Добавляет описание задачи"""
    logger.debug(f"state = {await state.get_state()}, handler text phase editing!")

    bot = await get_jedy(message.from_user.id, state)
    data = await state.get_data()
    bot.update_task_description(data['task'].id, message.text)

    answer_message = (
        f"Описание задачи дополнено.\n")
    await message.answer(answer_message)

@dp.message_handler(state='*', content_types=types.ContentTypes.TEXT)
async def add_task(message: types.Message, state: FSMContext):
    """Добавляет новую задачу"""
    logger.debug(f"state = {await state.get_state()} text handler!")

    bot = await get_jedy(message.from_user.id, state)
    task = bot.add(message.text)

    answer_message = (
        f"Задачу эту теперь легко сделать будет.\n")
    await message.answer(answer_message)
