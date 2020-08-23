import exceptions
from tasklist import TaskListBot, TaskStage
from phase import Phase

from keyboards import get_keyboard, review_keyboard
from aiogram import types
from aiogram.dispatcher import FSMContext

from misc import dp, logger, get_jedy, replicas


@dp.message_handler(
        state='*', commands=['start', 'help', 'howto', 'dzen', 'man'])
async def send_welcome(message: types.Message, state: FSMContext):
    """Show hello message to help with bot"""
    logger.debug(f"Send welcome handler text: {message.text} !")

    jbot = await get_jedy(message.from_user.id, state)
    logger.info(f"is new user? {jbot.new_user(message.from_user.username)}")

    key = message.text
    if key == '/start':
        key = '/help'
    await message.answer(replicas[key])


@dp.message_handler(state='*', commands=['todo', 'ideas', 'archive'])
async def full_task_list(message: types.Message, state: FSMContext):
    """Show tasklist for a stage"""
    logger.debug(f"Commands handler {message.text}")
    jbot = await get_jedy(message.from_user.id, state)

    stage = TaskStage(['/ideas', '/todo', '/archive'].index(message.text))
    await state.set_state(Phase.get(stage))

    full_list = jbot.tasks_list(stage)
    if not full_list:
        await message.answer(replicas['empty_list'][str(stage.value)])
        return

    to_post = [(i.id, i.text) for i in full_list]
    text = f"{replicas['list'][str(stage)]} ({len(to_post)})"
    await message.answer(text, reply_markup=get_keyboard(to_post))


@dp.message_handler(state='*', commands=['review'])
async def review(message: types.Message, state: FSMContext):
    """Show todo tasklist to review tasks"""
    logger.info(f"Review handler {message.text}")
    jbot = await get_jedy(message.from_user.id, state)

    stage = TaskStage.TODO
    await state.set_state(Phase.get(stage))
    full_list = jbot.tasks_list(stage)
    if not full_list:
        await message.answer(replicas['empty_list'][str(stage.value)])
        return

    to_post = [(i.id, i.text) for i in full_list]
    await message.answer(
        replicas['review'],
        reply_markup=review_keyboard(to_post))


@dp.message_handler(state='*', commands=['tag'])
async def tag(message: types.Message, state: FSMContext):
    """Show task for the tag"""
    logger.info(f"Tag handler {message.text}")
    jbot = await get_jedy(message.from_user.id, state)
    tag = message.text.split()[1]

    stage = await Phase.get_stage(state)
    full_list = jbot.tag_list(tag, stage)
    if not full_list:
        await message.answer(replicas['no_task4tag'])
        return

    to_post = [(i.id, i.text) for i in full_list]
    text = f"{replicas['tag_tasks']} {tag} ({str(len(to_post))})"
    await message.answer(text, reply_markup=get_keyboard(to_post))


@dp.message_handler(state='*', commands=['days'])
async def tag(message: types.Message, state: FSMContext):
    """ Set days parameter to X """
    logger.info(f"Tag handler {message.text}")
    jbot = await get_jedy(message.from_user.id, state)
    try:
        x = int(message.text.split()[1])
    except ValueError:
        await message.answer(replicas['wrong_days'])
        return

    jbot.update_days(x)
    await message.answer(replicas['days'])
