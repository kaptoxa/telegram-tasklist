from aiogram import types
from aiogram.utils.exceptions import MessageNotModified, Throttled


from misc import dp


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True

