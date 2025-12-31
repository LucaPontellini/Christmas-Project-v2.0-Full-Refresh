import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "instance", "database.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def query_one(query, params=()):
    with get_connection() as conn:
        cur = conn.execute(query, params)
        return cur.fetchone()


def query_all(query, params=()):
    with get_connection() as conn:
        cur = conn.execute(query, params)
        return cur.fetchall()


def execute(query, params=()):
    with get_connection() as conn:
        cur = conn.execute(query, params)
        conn.commit()
        return cur.lastrowid


def executemany(query, params_list):
    with get_connection() as conn:
        cur = conn.executemany(query, params_list)
        conn.commit()
        return cur.rowcount