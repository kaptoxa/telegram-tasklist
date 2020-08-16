import logging

import os
from tasklist import TaskListBot

from aiogram import Bot, Dispatcher, types
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.utils.helper import Helper, HelperMode, ListItem



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Phase(Helper):
    mode = HelperMode.snake_case

    IDEAS = ListItem()
    TASKS = ListItem()
    ARCHIVE = ListItem()
    EDIT_IDEA = ListItem()
    EDIT_TASK = ListItem()
    EDIT_ARCH = ListItem()



todo_cb = CallbackData('todo', 'id', 'action')  # post:<id>:<action>
task_cb = CallbackData('task', 'id', 'action')  # post:<id>:<action>

"""
chats = {}

def get_jedy(chat_id):
    if chat_id not in chats:
        chats[chat_id] = TaskListBot(chat_id)
    return chats[chat_id]

async def shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info('Storage is closed!')
"""