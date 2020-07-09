import exceptions
from tasklist import TaskListBot
from aiogram import types
from pprint import pprint

from misc import dp, get_jedy


@dp.message_handler()
async def add_task(message: types.Message):
    chat_id = message.from_user.id
    bot = get_jedy(chat_id)

    """Добавляет новую задачу"""
    try:
        task = bot.add(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return

    pprint(task)
    answer_message = (
        f"Задачу эту теперь легко сделать будет.\n")
    await message.answer(answer_message)
#    await bot.send_message(message.chat.id, '\n'.join(['1. Task number x', '1. Task .. ', 'w3. Not task!']))
