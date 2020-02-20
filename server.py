"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import os

from aiogram import Bot, Dispatcher, executor, types

import exceptions
import task_list


logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = Bot(token=API_TOKEN) #, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для списка задач\n\n"
        "Добавить задачу: купить хлеба\n"
        "Вывести список: /all\n"
        "Провести обзор: /review")


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_task(message: types.Message):
    """Удаляет одну задачу по её идентификатору"""
    row_id = int(message.text[4:])
    task_list.delete_task(row_id)
    answer_message = "Удалил"
    await message.answer(answer_message)


@dp.message_handler(commands=['all'])
async def full_task_list(message: types.Message):
    """Отправляет весь список задач"""
    full_list= task_list.all()
    if not full_list:
        await message.answer("Не одбавлено ни одной задачи")
        return

    full_task_list= [
        f"{task.text} — нажми "
        f"/del{task.id} для удаления"
        for task in full_list]
    answer_message = "Весь список задач:\n\n* " + "\n\n* "\
            .join(full_task_list)
    await message.answer(answer_message)


@dp.message_handler()
async def add_task(message: types.Message):
    """Добавляет новую задачу"""
    try:
        task = task_list.add_task(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлена задача {task} .\n\n")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
