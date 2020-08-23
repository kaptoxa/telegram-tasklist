import logging

import os
import json

from tasklist import TaskListBot
from phase import Phase

from aiogram import Bot, Dispatcher, types
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

with open("replicas.json", "r") as r_file:
    replicas = json.load(r_file)


todo_cb = CallbackData('todo', 'id', 'action')  # post:<id>:<action>
task_cb = CallbackData('task', 'id', 'action')  # post:<id>:<action>


async def get_jedy(chat_id, state: FSMContext):
    """ while storage is memory
        we need to create TaskListBot object
        every time after restart """

    data = await state.get_data()
    if 'bot' not in data:
        new_bot = TaskListBot(chat_id)
        await state.update_data(bot=new_bot)
        await state.set_state(Phase.TASKS)
        return new_bot

    return data['bot']

