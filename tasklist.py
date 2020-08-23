""" We create one bot for one user to work with his tasks """
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
    """Tuple structure respondes a record in DB"""
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
        text, tags = _parse_message(raw_message)
        f_now = _get_now_formatted()
        inserted_row_id = db.insert("tasklist", {
            "stage": TaskStage.TODO.value,
            "created": f_now,
            "changed": f_now,
            "text": text,
            "tags": tags,
            "user_id": self.chat_id
        })
        return Task(id=None, text=text, tags=tags,
                    stage=TaskStage.TODO, created=f_now, changed=f_now)

    def update_task_stage(self, taskid: int, stage: TaskStage) -> bool:
        db.update("tasklist", {
                    "stage": stage.value,
                    "changed": f"\"{_get_now_formatted()}\""},
                    {"id": ("=", taskid)})
        return True

    def update_task_text(self, taskid: int, text: str) -> bool:
        db.update("tasklist", {
                    "text": f"\"{text}\"",
                    "changed": f"\"{_get_now_formatted()}\""},
                    {"id": ("=", taskid)})
        return True

    def update_days(self, days: int) -> bool:
        db.update("users", {"days": days},
                    {"id": ("=", self.chat_id)})
        return True

    def tasks(self) -> List[Task]:
        """ return all tasks """
        rows = db.fetchall("tasklist", ["*"],
                    {"user_id": ("=", self.chat_id)})
        task_list = [Task(*row[:-1]) for row in rows]
        # clip this field because this is chat id
        return task_list

    def tasks_list(self, stage: TaskStage) -> List[Task]:
        """ return tasks for the stage """
        return list(filter(lambda task: task.stage == stage.value, self.tasks()))

    def tag_list(self, tag: str, stage: TaskStage) -> List[Task]:
        return list(filter(lambda task: (tag in task.tags),
                self.tasks_list(stage)))

    def get_task(self, tid) -> Task:
        """ return the task by its id """
        row = db.fetchone("tasklist", ["*"],
                {"user_id": ("=", self.chat_id),
                "id": ("=", tid)})
        if row:
            task = Task(*row[:-1])
            return task
        else:
            raise exceptions.NotCorrectTaskID("getting task...")
        return


    def delete_task(self, row_id: int) -> None:
        db.delete("tasklist", row_id)


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _parse_message(msg):
    """ tags are words that started with '#' """
    task = []
    tags = []
    for word in msg.split():
        if word[0] == '#':
            tags += [word]
        else:
            task += [word]
    return ' '.join(task), ' '.join(tags)
