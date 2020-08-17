""" Telegram bot server to run"""
from aiogram import executor, Dispatcher

from misc import dp, logger
import handlers


async def shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info('Storage is closed!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
