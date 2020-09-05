from aiogram import types
from misc import todo_cb

def tasks(tasks, tags) -> types.InlineKeyboardMarkup:
    """ generate keyboard from tasklist """
    markup = types.InlineKeyboardMarkup()
    for tid, text in tasks:
        markup.add(
            types.InlineKeyboardButton(
                text,
                callback_data=todo_cb.new(id=tid, action='view', tags=tags)),
        )
    return markup


def review(tasks) -> types.InlineKeyboardMarkup:
    """ generate review keyboard """
    markup = types.InlineKeyboardMarkup()
    for tid, text in tasks:
        markup.row(
            types.InlineKeyboardButton(
                text,
                callback_data=todo_cb.new(id=tid, action='review_done')),
        )
    return markup


def tags(tags) -> types.InlineKeyboardMarkup:
    """ generate tags keyboard """
    markup = types.InlineKeyboardMarkup()
    for tag in tags:
        if tag:
            markup.row(
                types.InlineKeyboardButton(
                    tag,
                    callback_data=todo_cb.new(id=tag, action='tasks_by_tag', tags='')),
            )
    return markup
