import logging

import os
from tasklist import TaskListBot

from aiogram import Bot, Dispatcher, types
from aiogram.utils.callback_data import CallbackData



logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)

todo_cb = CallbackData('todo', 'id', 'action')  # post:<id>:<action>
task_cb = CallbackData('task', 'id', 'action')  # post:<id>:<action>


chats = {}

def get_jedy(chat_id):
    if chat_id not in chats:
        chats[chat_id] = TaskListBot(chat_id)
    return chats[chat_id]
