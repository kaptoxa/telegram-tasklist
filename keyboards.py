from aiogram import types
from misc import todo_cb

def get_keyboard(tasks) -> types.InlineKeyboardMarkup:
    """ generate keyboard from tasklist """
    markup = types.InlineKeyboardMarkup()
    for tid, text in tasks:
        markup.add(
            types.InlineKeyboardButton(
                text,
                callback_data=todo_cb.new(id=tid, action='view')),
        )
    return markup


def review_keyboard(tasks) -> types.InlineKeyboardMarkup:
    """ generate review keyboard """
    markup = types.InlineKeyboardMarkup()
    for tid, text in tasks:
        markup.row(
            types.InlineKeyboardButton(
                text,
                callback_data=todo_cb.new(id=tid, action='review_done')),
        )
    return markup


