""" Работа с задачами— их добавление, удаление, завершение"""
import datetime
from typing import List, NamedTuple, Optional
from pprint import pprint

import pytz

import db
import exceptions



class Task(NamedTuple):
    """Структура добавленной в БД новой задачи"""
    id: Optional[int]
    done: bool
    marked: bool
    idea: bool
    created: str
    completed: str
    text: str
    description: str


class TaskListBot():

    def __init__(self, chat_id):
        self.chat_id = chat_id


    def add(self, raw_message: str) -> Task:
        """Добавляет задачу"""
        #parsed_message = _parse_message(raw_message)
        f_now = _get_now_formatted()
        inserted_row_id = db.insert("tasklist", {
            "done": False,
            "marked": False,
            "idea": False,
            "created": f_now,
            "completed": f_now,
            "text": raw_message,
            "description": raw_message,
            "user_id": self.chat_id
        })
        return Task(id=None,
                text=raw_message, description=raw_message, done=False, marked=False, idea=False, created=f_now, completed=f_now)


    def done(self, taskid: int) -> Task:
#        updated_row_id = db.update()
#        return Task(id=None,
#                text='', description=raw_message, done=True, marked=False, idea=False, created=f_now, completed=f_now)
        return None


    def idea(self, taskid: int) -> Task:
#       updated_row_id = db.update()
#        return Task(id=None,
#                text=raw_message, description=raw_message, done=False, marked=False, idea=True, created=f_now, completed=f_now)
        return None


    
    def all(self) -> List[Task]:
        """Возвращает все задачи"""
        cursor = db.get_cursor()
        cursor.execute( f"select * from tasklist where user_id=={self.chat_id}")
        rows = cursor.fetchall()
        task_list = [Task(*row[:-1]) for row in rows]  # отсекаем последнее поле, т.к. это chat id
        return task_list


    def starred(self) -> List[Task]:
        """Возвращает отмеченные задачи"""
        return [filter(lambda task: task.marked == True, all())]


    def ideas(self) -> List[Task]:
        """Возвращает отмеченные задачи"""
        return [filter(lambda task: task.idea == True, all())]


    def get_task(self, tid) -> Task:
        """Возвращает задачу по её id"""
        cursor = db.get_cursor()
        cursor.execute( f"select * from tasklist where user_id=={self.chat_id} and id={tid}")
        row = cursor.fetchone()
        if row:
            task = Task(*row[:-1])
            return task
        else:
            raise exceptions.NotCorrectTaskID("getting task...")
        return


    def delete_task(self, row_id: int) -> None:
        """Удаляет задачу по её идентификатору"""
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

