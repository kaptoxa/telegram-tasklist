import logging

import os
import json

from tasklist import TaskListBot

from aiogram import Bot, Dispatcher, types
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
#from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.utils.helper import Helper, HelperMode, ListItem



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

with open("replicas.json", "r") as r_file:
    replicas = json.load(r_file)

# States
class Phase(Helper):
    mode = HelperMode.snake_case

    IDEAS = ListItem()
    TASKS = ListItem()
    ARCHIVE = ListItem()
    EDIT_IDEA = ListItem()
    EDIT_TASK = ListItem()
    EDIT_ARCH = ListItem()

    def get(stage):
    #  trick to avoid sorted items problem that Helper does alphabetically
        return Phase.all()[(stage + 4) % 6]




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

