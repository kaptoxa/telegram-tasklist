""" Работа с задачами— их добавление, удаление, завершение"""
import datetime
from typing import List, NamedTuple, Optional

import pytz

import db
import exceptions


#class Message(NamedTuple):
#    """Структура распаршенного сообщения о новой задаче"""
#    task: str
#    project: str


class Task(NamedTuple):
    """Структура добавленной в БД новой задачи"""
    id: Optional[int]
    done: bool
    marked: bool
    text: str


def add_task(raw_message: str, user_id: int) -> Task:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    #parsed_message = _parse_message(raw_message)
    inserted_row_id = db.insert("tasklist", {
        "text": raw_message,
        "created": _get_now_formatted(),
        "done": False,
        "marked": False,
        "user_id": user_id
    })
    return Task(id=None,
                   text=raw_message, done=False, marked=False)


def all(user_id: int) -> List[Task]:
    """Возвращает все задачи"""
    cursor = db.get_cursor()
    cursor.execute( f"select id, text, done, marked from tasklist where user_id=={user_id}")
    rows = cursor.fetchall()
    task_list = [Task(id=row[0], text=row[1], done=row[2], marked=row[3]) for row in rows]
    return task_list


def delete_task(row_id: int) -> None:
    """Удаляет сообщение по его идентификатору"""
    db.delete("tasklist", row_id)


#def _parse_message(raw_message: str) -> Message:
#    """Парсит текст пришедшего сообщения о новой задаче."""
            #raise exceptions.NotCorrectMessage(
            #    "Не могу понять сообщение. Не используйте больше одной точки. "
            #    "например:\nНаписать заявление. Подготовка к школе"
            #    "Написать заявление - задача, Подготовка к школе - проект")
#    task = raw_message
#
#    return Message(task=task)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now

