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
    created: str
    changed: str
    text: str
    tags: str


class TaskListBot():

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def new_user(self, name):
        """ new user """
        cursor = db.get_cursor()
        cursor.execute( f"select * from users where id={self.chat_id}")
        row = cursor.fetchone()
        if row:
            return False

        inserted_row_id = db.insert("users", {
            "id": self.chat_id,
            "name": name,
            "days": 1
        })
        return inserted_row_id

    def add(self, raw_message: str) -> Task:
        """ new task """
        f_now = _get_now_formatted()
        inserted_row_id = db.insert("tasklist", {
            "stage": TaskStage.TODO.value,
            "created": f_now,
            "changed": f_now,
            "text": raw_message,
            "tags": raw_message,
            "user_id": self.chat_id
        })
        return Task(id=None,
                text=raw_message, tags='', stage=TaskStage.TODO, created=f_now, changed=f_now)

    def update_task_stage(self, taskid: int, stage: TaskStage) -> bool:
        cursor = db.get_cursor()
        print(stage)
        cursor.execute(
            f"update tasklist set stage = {stage.value}, "
            f"changed = \"{_get_now_formatted()}\" "
            f"where tasklist.id = {taskid}" )
        db.get_connection().commit()
        return True

    def update_task_text(self, taskid: int, text: str) -> bool:
        cursor = db.get_cursor()
        cursor.execute(
                f"update tasklist set text=\"{text}\","
                f"changed=\"{_get_now_formatted()}\" "
                f"where tasklist.id={taskid}")
        db.get_connection().commit()
        return True

    def update_days(self, days: int) -> bool:
        cursor = db.get_cursor()
        cursor.execute(
                f"update users set days={days} "
                f"where users.id={self.chat_id}")
        db.get_connection().commit()
        return True

    def tasks(self) -> List[Task]:
        """ return all tasks """
        cursor = db.get_cursor()
        cursor.execute( f"select * from tasklist where user_id=={self.chat_id}")
        rows = cursor.fetchall()
        task_list = [Task(*row[:-1]) for row in rows]  # отсекаем последнее поле, т.к. это chat id
        return task_list

    def tasks_list(self, stage: TaskStage) -> List[Task]:
        """ return tasks for the stage """
        return list(filter(lambda task: task.stage == stage, self.tasks()))

    def get_task(self, tid) -> Task:
        """ return the task by its id """
        cursor = db.get_cursor()
        cursor.execute( f"select * from tasklist where user_id={self.chat_id} and id={tid}")
        row = cursor.fetchone()
        if row:
            task = Task(*row[:-1])
            return task
        else:
            raise exceptions.NotCorrectTaskID("getting task...")
        return


    def delete_task(self, row_id: int) -> None:
        db.delete("tasklist", row_id)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now

