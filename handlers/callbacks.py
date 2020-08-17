from tasklist import TaskListBot, Task, TaskStage

from keyboards import get_keyboard
from aiogram import types, md
from aiogram.dispatcher import FSMContext

from misc import bot, dp, todo_cb, task_cb, Phase, logger, get_jedy



def format_post(task: Task) -> (str, types.InlineKeyboardMarkup):
    logger.debug(f" format_post :: {task.description}")

    text = md.text(
        md.hbold(task.text), '',
        md.quote_html(task.description),'',
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
    markup.row( *all_buttons.values())
    markup.add(types.InlineKeyboardButton('<< Back', callback_data=task_cb.new(id=task.id, action='list')))
    return text, markup


async def show_tasklist(query: types.CallbackQuery, stage, state: FSMContext):
    """Отправляет весь список задач"""
    logger.debug(f"show_tasklist :: stage = {stage}")

    jbot = await get_jedy(query.from_user.id, state)
    full_list = jbot.tasks_list(stage.value)
    if not full_list:
        empty_message = {0: "Нет идей? Хватит медитировать!", 1: "Список задач пуст", 2: "Архив пуст"}
        await query.message.answer(empty_message[stage.value])
        return

    await state.set_state(Phase.get(stage.value))

    to_post = [(i.id, i.text) for i in full_list]
    list_name = {0: "Список идей", 1: "Список задач", 2: "Архив"}
    await query.message.edit_text(list_name[stage.value],
            reply_markup=get_keyboard(to_post))


@dp.callback_query_handler(task_cb.filter(action='list'), state='*')
async def query_list(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    logger.debug(f"query_list cur_state = {cur_state}")

    stage = TaskStage.TODO
    cur_state = await state.get_state()
    if Phase.EDIT_IDEA[0] in cur_state:
        stage = TaskStage.IDEA
    elif Phase.EDIT_ARCH[0] in cur_state:
        stage = TaskStage.DONE

    await show_tasklist(query, stage, state)


@dp.callback_query_handler(todo_cb.filter(action='view'), state='*')
async def query_view(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    logger.debug(f"handlers/callback view task id = {task_id}!")

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

    text, markup = format_post(task)
    await query.message.edit_text(text, reply_markup=markup)  #, parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(task_cb.filter(action=['done', 'idea', 'todo', 'cancel']), state='*')
async def query_taskedit(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
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

    await query.answer('Задача изменена.')

    stage = TaskStage.TODO
    cur_state = await state.get_state()
    if Phase.EDIT_IDEA[0] in cur_state:
        stage = TaskStage.IDEA
    elif Phase.EDIT_ARCH[0] in cur_state:
        stage = TaskStage.DONE

    await show_tasklist(query, stage, state)
