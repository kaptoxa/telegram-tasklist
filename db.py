"""
Now we use sqlite3 for db, but we should be able to change it,
that's why we have this file.
"""
import os
from typing import Dict, List, Tuple

import sqlite3

conn = sqlite3.connect(os.path.join("db", "jedidb.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def update(table: str, column_values, conditions: Dict):
    changes = ', '.join(f"{key}={value}"
                        for key, value in column_values.items())
    condition = ' AND '.join(f"{key} {oper} {value}"
                        for key, (oper, value) in conditions.items())
    cursor.execute(
        f"UPDATE {table} SET {changes} "
        f"WHERE {condition}")
    conn.commit()


def fetchall(table: str, columns: List[str], conditions: Dict) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    condition = ' AND '.join(f"{key} {oper} {value}"
                for key, (oper, value) in conditions.items()) if conditions else ''
    cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE {condition}")
    return cursor.fetchall()


def fetchone(table: str, columns: List[str], conditions: Dict) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    condition = ' AND '.join(f"{key} {oper} {value}"
                for key, (oper, value) in conditions.items()) if conditions else ''
    cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE {condition}")
    return cursor.fetchone()


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def get_connection():
    return conn


def _init_db():
    """ Initializing database """
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """ if database was not created then we have to do it """
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='tasklist'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()
