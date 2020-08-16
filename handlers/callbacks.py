# from remote_db import get_customer, get_orders_by_cid
from keyboards import get_keyboard
from aiogram import types, md
from aiogram.dispatcher import FSMContext
from tasklist import TaskListBot, Task, TaskStage

from misc import bot, dp, todo_cb, task_cb, Phase, logger



def format_post(task: Task) -> (str, types.InlineKeyboardMarkup):
    text = md.text(
        md.hbold(task.text),
        md.quote_html(task.description),
        '',  # just new empty line
        f"Создана: {task.created}",
        sep = '\n',
    )

    all_buttons = {2:  types.InlineKeyboardButton('Сделано!',
        callback_data=task_cb.new(id=task.id, action='done')),
        0: types.InlineKeyboardButton('В идеи!',
            callback_data=task_cb.new(id=task.id, action='idea')),
        1: types.InlineKeyboardButton('В задачи!',
            callback_data=task_cb.new(id=task.id, action='todo')),
        'cancel': types.InlineKeyboardButton('Удалить.',
            callback_data=task_cb.new(id=task.id, action='cancel'))
        }

    del all_buttons[task.stage]

    markup = types.InlineKeyboardMarkup()
    markup.row( *all_buttons.values()
#        types.InlineKeyboardButton('Сделано!', callback_data=task_cb.new(id=task.id, action='done')),
#        types.InlineKeyboardButton('В идеи!', callback_data=task_cb.new(id=task.id, action='idea')),
#        types.InlineKeyboardButton('Удалить.', callback_data=task_cb.new(id=task.id, action='cancel')),
    )
    markup.add(types.InlineKeyboardButton('<< Back', callback_data=task_cb.new(id=task.id, action='list')))
    return text, markup


async def show_tasklist(query: types.CallbackQuery, chat_id, stage, state: FSMContext):
    """Отправляет весь список задач"""
    data = await state.get_data()
    jbot = data['bot']
    logger.info(stage)
    full_list = jbot.tasks_list(stage.value)
    if not full_list:
        await query.message.answer(f"{stage} Сконцентрируйся и оставайся внимательным.")
        return

    to_post = [(i.id, i.text) for i in full_list]
    await query.message.edit_text(f"Задачи ваши Вам делать. {stage}",
            reply_markup=get_keyboard(to_post))


@dp.callback_query_handler(task_cb.filter(action='list'), state='*')
async def query_list(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    logger.info(f"query_list1 {state.get_state()}")
    stage = TaskStage.TODO
    cur_state = await state.get_state()
    logger.info(f"cur_state = {cur_state}, Phase.EDIT_IDEA = {Phase.EDIT_IDEA[0]}")
    if Phase.EDIT_IDEA[0] in cur_state:
        stage = TaskStage.IDEA
    elif Phase.EDIT_ARCH[0] in cur_state:
        stage = TaskStage.DONE

    await show_tasklist(query, query.from_user.id, stage, state)


"""
@dp.callback_query_handler(task_cb.filter(action='list'), state=Phase.EDIT_IDEA)
async def query_list(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    logger.info(f"query_list2 {state.get_state()}")
    await show_tasklist(query, query.from_user.id, TaskStage.IDEA)


@dp.callback_query_handler(task_cb.filter(action='list'), state=Phase.EDIT_ARCH)
async def query_list(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    logger.info(f"query_list3 {state}")
    await show_tasklist(query, query.from_user.id, TaskStage.DONE)
"""


@dp.callback_query_handler(todo_cb.filter(action='view'), state='*')
async def query_view(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    task_id = int(callback_data['id'])
    data = await state.get_data()
    jbot = data['bot']

    logger.info(f"handlers/callback view task id = {task_id}!")
    task = jbot.get_task(task_id)
    if not task:
        return await query.answer('Error!')

    await state.update_data(task=task)
    logger.info(f"task = {task.stage}")

    stage = TaskStage(task.stage)
    if stage == TaskStage.TODO:
        await state.set_state(Phase.EDIT_TASK[0])
    elif stage == TaskStage.IDEA:
        await state.set_state(Phase.EDIT_IDEA[0])
    elif stage == TaskStage.DONE:
        await state.set_state(Phase.EDIT_ARCH[0]) 

    text, markup = format_post(task)
    await query.message.edit_text(text, reply_markup=markup)  #, parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(task_cb.filter(action=['done', 'idea', 'todo', 'cancel']), state='*')
async def query_taskedit(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    task_id = int(callback_data['id'])
    action = callback_data['action']
    data = await state.get_data()
    jbot = data['bot']

    task = jbot.get_task(task_id)
    if not task:
        return await query.answer('Error!')

    if action == 'cancel':
        jbot.delete_task(task.id)
    else:
        i = ['idea', 'todo', 'done'].index(action)
        jbot.update_task_stage(task.id, TaskStage(i))

    await query.answer('Задача изменена.')

    stage = TaskStage.TODO
    cur_state = await state.get_state()
    logger.info(f"cur_state = {cur_state}, Phase.EDIT_IDEA = {Phase.EDIT_IDEA[0]}")
    if Phase.EDIT_IDEA[0] in cur_state:
        print('!!!')
        stage = TaskStage.IDEA
    elif Phase.EDIT_ARCH[0] in cur_state:
        stage = TaskStage.DONE

    await show_tasklist(query, chat_id, stage, state)
#     await query_list(query, callback_data=tcb) #  task_cb.new(id=task.id, action='list'))

