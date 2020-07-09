#from remote_db import get_customer, get_orders_by_cid
from keyboards import get_keyboard
from aiogram import types, md
from tasklist import TaskListBot, Task

from misc import bot, dp, todo_cb, task_cb, get_jedy



def format_post(task: Task) -> (str, types.InlineKeyboardMarkup):
    text = md.text(
        md.hbold(task.text),
        md.quote_html(task.description),
        '',  # just new empty line
        f"Создана: {task.created}",
        sep = '\n',
    )

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('Сделано!', callback_data=task_cb.new(id=task.id, action='done')),
        types.InlineKeyboardButton('В идеи!', callback_data=task_cb.new(id=task.id, action='idea')),
        types.InlineKeyboardButton('Удалить.', callback_data=task_cb.new(id=task.id, action='cancel')),
    )
    markup.add(types.InlineKeyboardButton('<< Back', callback_data=task_cb.new(id='-', action='list')))
    return text, markup


@dp.callback_query_handler(task_cb.filter(action='list'))
async def query_view(query: types.CallbackQuery, callback_data: dict):
    chat_id = query.from_user.id
    jbot = get_jedy(chat_id)

    """Отправляет весь список задач"""
    full_list = jbot.all()
    if not full_list:
        await message.answer("Не одбавлено ни одной задачи")
        return

    to_post = [(i.id, i.text) for i in full_list]
    await query.message.edit_text('Задачи ваши Вам делать.', reply_markup=get_keyboard(to_post))


@dp.callback_query_handler(todo_cb.filter(action='view'))
async def query_view(query: types.CallbackQuery, callback_data: dict):
    task_id = int(callback_data['id'])
    chat_id = query.from_user.id
    jbot = get_jedy(chat_id)

    task = jbot.get_task(task_id)
    if not task:
        return await query.answer('Error!')

    text, markup = format_post(task)
    await query.message.edit_text(text, reply_markup=markup)  #, parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(task_cb.filter(action=['done', 'idea', 'cancel']))
async def query_taskedit(query: types.CallbackQuery, callback_data: dict):
    task_id = int(callback_data['id'])
    action = callback_data['action']
    jbot = get_jedy(query.from_user.id)

    task = jbot.get_task(int(task_id))
    if not task:
        return await query.answer('Error!')

    if action == 'done':
        """Сделать отправку задачи в архив (добавить поле в базу)"""
        print('Обновляем задачу в базе')
        jbot.done(task_id)
    elif action == 'idea':
        """Помещаем задачу в идеи (обновить поле в базе)"""
        print('Обновляем задачу в базе')
        jbot.idea(task_id)
    elif action == 'cancel':
        """Отменяем задачу, она окончательно пропадает"""
        jbot.delete_task(task.id)
    
        full_list = jbot.all()
        if not full_list:
            await query.message.edit_text("Туманным будущее ваше является.")
            return

        to_post = [(i.id, i.text) for i in full_list]
        await query.message.edit_text('Задачи ваши Вам делать.', reply_markup=get_keyboard(to_post))

    await query.answer('Задача изменена.')

#
#@dp.errors_handler(exception=MessageNotModified)
#async def message_not_modified_handler(update, error):
#    return True


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
