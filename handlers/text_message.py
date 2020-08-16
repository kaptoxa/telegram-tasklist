import exceptions
from tasklist import TaskListBot
from aiogram import types
from aiogram.dispatcher import FSMContext
from misc import Phase, dp, logger


@dp.message_handler(state=Phase.EDIT_TASK | Phase.EDIT_IDEA | Phase.EDIT_ARCH)
async def add_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot = data['bot']

    cur_state = await state.get_state()
    logger.info(f"state = {cur_state}, handler text phase editing!")

    """Добавляет описание задачи"""
    bot.update_task_description(data['task'].id, message.text)

    answer_message = (
        f"Описание задачи дополнено.\n")
    await message.answer(answer_message)

@dp.message_handler(state='*', content_types=types.ContentTypes.TEXT)
async def add_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot = data['bot']

    cur_state = await state.get_state()
    logger.info(f"state = {cur_state} text handler!")

    """Добавляет новую задачу"""
    task = bot.add(message.text)

    answer_message = (
        f"Задачу эту теперь легко сделать будет.\n")
    await message.answer(answer_message)
