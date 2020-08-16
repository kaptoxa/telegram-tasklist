from aiogram import types
from misc import todo_cb

def get_keyboard(tasks) -> types.InlineKeyboardMarkup:
    """
    Генерирует клавиатуру из списка задач
    """
    markup = types.InlineKeyboardMarkup()
    for tid, text in tasks:
        markup.add(
            types.InlineKeyboardButton(
                text,
                callback_data=todo_cb.new(id=tid, action='view')),
        )
    return markup
