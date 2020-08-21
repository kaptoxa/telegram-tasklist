import schedule
import time

from datetime import datetime
import pytz

import db


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime:
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz)
    return now

def land_user(uid, days):
    """ life lands users because they soaring in the clouds """
    cursor = db.get_cursor()
    cursor.execute(
            "select id, changed from tasklist "
            f"where user_id={uid} and stage=1")
    rows = cursor.fetchall()
    if not rows:
        return

    now = _get_now_datetime()
    task_to_ideas = []
    for tid, changed in rows:
        print(f"task {tid} was changed at {changed}")
        task_changed = datetime.strptime(changed, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.timezone("Europe/Moscow"))
        delta = task_changed - now
        if delta.days > days:
            task_to_ideas += [str(tid)]

    if task_to_ideas:
        print(f"tick... some tasks left to ideas. {_get_now_formatted()}")
        cursor.execute(
            "update tasklist set stage=0 "
            f"where tasklist.id in ({', '.join(task_to_ideas)})")


def life():
    cursor = db.get_cursor()
    cursor.execute( "select * from users")
    users = cursor.fetchall()
    if users:
        for uid, name, days in users:
            print(f"user: {name}, telegram id: {uid}, days = {days}")
            land_user(uid, days)

    db.get_connection().commit()


schedule.every().day.do(life)

while True:
    schedule.run_pending()
    time.sleep(3600 *24)
