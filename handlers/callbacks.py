from tasklist import TaskListBot, Task, TaskStage
from phase import Phase

import keyboards
from aiogram import types, md
from aiogram.dispatcher import FSMContext

from misc import logger, bot, dp, todo_cb, task_cb
from misc import get_jedy, replicas


def format_post(task: Task, tags: str) -> (str, types.InlineKeyboardMarkup):
    logger.debug(f" format_post :: {task.text}")

    text = md.text(
        md.hbold(task.text), '', md.hbold('tags:', task.tags),
        f"{replicas['task']['created_date']}: {task.created}",
        f"{replicas['task']['changed_date']}: {task.changed}",
        sep='\n',
    )

    all_buttons = {
        TaskStage.DONE: types.InlineKeyboardButton(
            replicas['task']['done'],
            callback_data=task_cb.new(id=task.id, action='done', tags=tags)),
        TaskStage.IDEA: types.InlineKeyboardButton(
            replicas['task']['idea'],
            callback_data=task_cb.new(id=task.id, action='idea', tags=tags)),
        TaskStage.TODO: types.InlineKeyboardButton(
            replicas['task']['todo'],
            callback_data=task_cb.new(id=task.id, action='todo', tags=tags)),
        'cancel': types.InlineKeyboardButton(
            replicas['task']['cancel'],
            callback_data=task_cb.new(id=task.id, action='cancel', tags=tags))
        }
    del all_buttons[TaskStage(task.stage)]

    markup = types.InlineKeyboardMarkup()
    markup.row(*all_buttons.values())
    markup.add(
        types.InlineKeyboardButton(
            '<< Back',
            callback_data=task_cb.new(id=task.id, action='list', tags=tags)))
    return text, markup


async def show_tasklist(tags, query: types.CallbackQuery, state: FSMContext):
    """Fill whole tasklist"""

    logger.info(f'show taskl {tags}')
    jbot = await get_jedy(query.from_user.id, state)
    stage = await Phase.get_stage(state)

    full_list = jbot.tasks_by_tag(set(tags.split()), stage) if tags else jbot.tasks_list(stage)
    if not full_list:
        await query.message.answer(replicas['empty_list'][str(stage)])
        return

    await state.set_state(Phase.get(stage))

    to_post = [(i.id, i.text) for i in full_list]
    text = f"{replicas['list'][str(stage)]} ({len(to_post)})"
    await query.message.edit_text(text,
                                  reply_markup=keyboards.tasks(to_post, tags))


@dp.callback_query_handler(task_cb.filter(action='list'), state='*')
async def query_list(
        query: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext):

    await show_tasklist(callback_data['tags'], query, state)


@dp.callback_query_handler(todo_cb.filter(action='view'), state='*')
async def query_view(
        query: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext):

    logger.info(f"callback_data['tags'] = {callback_data['tags']}")
    task_id = int(callback_data['id'])
    jbot = await get_jedy(query.from_user.id, state)
    task = jbot.get_task(task_id)
    if not task:
        return await query.answer('Error!')

    await state.update_data(task=task)
    stage = TaskStage(task.stage)
    if stage == TaskStage.TODO:
        await state.set_state(Phase.EDIT_TASK[0])
    elif stage == TaskStage.IDEA:
        await state.set_state(Phase.EDIT_IDEA[0])
    elif stage == TaskStage.DONE:
        await state.set_state(Phase.EDIT_ARCH[0])

    text, markup = format_post(task, callback_data['tags'])
    await query.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(
        task_cb.filter(action=['done', 'idea', 'todo', 'cancel']),
        state='*')
async def query_taskedit(
        query: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext):

    task_id = int(callback_data['id'])
    action = callback_data['action']

    jbot = await get_jedy(query.from_user.id, state)
    task = jbot.get_task(task_id)
    if not task:
        return await query.answer('Error!')

    if action == 'cancel':
        jbot.delete_task(task.id)
    else:
        i = ['idea', 'todo', 'done'].index(action)
        jbot.update_task_stage(task.id, TaskStage(i))

    await query.answer(replicas['task']['changed'])
    await show_tasklist(callback_data['tags'], query, state)


@dp.callback_query_handler(todo_cb.filter(action=['review_done']), state='*')
async def query_task_done(
        query: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext):

    task_id = int(callback_data['id'])
    logger.info(f"query_task_done: {task_id}")
    jbot = await get_jedy(query.from_user.id, state)

    task = jbot.get_task(task_id)
    if not task:
        return await query.answer('Error!')
    jbot.update_task_stage(task.id, TaskStage(2))

    full_list = jbot.tasks_list(1)
    if not full_list:
        await query.message.edit_text(replicas['victory'])
        return

    to_post = [(i.id, i.text) for i in full_list]
    await query.message.edit_text(
        replicas['review'],
        reply_markup=review_keyboard(to_post))


@dp.callback_query_handler(task_cb.filter(action=['tasks_by_tag']), state='*')
async def show_me_tag(
        query: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext):

    tag = callback_data['id']
    logger.info(f"tasks_by_tag... {tag}!")
    jbot = await get_jedy(query.from_user.id, state)

    full_list = jbot.tasks_list(1)
    if not full_list:
        await query.message.edit_text(replicas['victory'])
        return

    to_post = [(i.id, i.text) for i in full_list]
    await query.message.edit_text(
        replicas['review'],
        reply_markup=review_keyboard(to_post))
