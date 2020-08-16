""" Работа с задачами— их добавление, удаление, завершение"""
import datetime
from typing import List, NamedTuple, Optional

import pytz

import db
import exceptions
from enum import Enum


class TaskStage(Enum):
    TODO = 1
    IDEA = 0
    DONE = 2


class Task(NamedTuple):
    """Структура соотвествует записи в БД"""
    id: Optional[int]
    stage: TaskStage
    marked: bool
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
            "stage": TaskStage.TODO.value,
            "marked": False,
            "created": f_now,
            "completed": f_now,
            "text": raw_message,
            "description": raw_message,
            "user_id": self.chat_id
        })
        return Task(id=None,
                text=raw_message, description=raw_message, stage=TaskStage.TODO, marked=False, created=f_now, completed=f_now)


    def update_task_stage(self, taskid: int, stage: TaskStage) -> bool:
        cursor = db.get_cursor()
        cursor.execute(
            f"update tasklist set stage={stage.value} "
            f"where tasklist.id={taskid}" )
        return True


    def update_task_description(self, taskid: int, description: str) -> bool:
        cursor = db.get_cursor()
        cursor.execute(
                f"update tasklist set description=\"{description}\" "
                f"where tasklist.id={taskid}")
        return True


    def tasks(self) -> List[Task]:
        """Возвращает все задачи"""
        cursor = db.get_cursor()
        cursor.execute( f"select * from tasklist where user_id=={self.chat_id}")
        rows = cursor.fetchall()
        task_list = [Task(*row[:-1]) for row in rows]  # отсекаем последнее поле, т.к. это chat id
        return task_list


    def tasks_list(self, stage: TaskStage) -> List[Task]:
        """Возвращает активные задачи"""
        return list(filter(lambda task: task.stage == stage, self.tasks()))

    def starred(self) -> List[Task]:
        """Возвращает отмеченные задачи"""
        return list(filter(lambda task: task.marked, self.tasks()))


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


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now

