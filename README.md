Telegram бот для ведения списка задач.


В переменных окружения надо проставить API токен бота.

`API_TOKEN` — API токен бота


Бот запускается двумя скриптами:
server.py - непосредственно бот
life.py - скрипт, обновляющий состояние невыполненных задач: если на задачу не сделан обзор, она уходит в идеи.

