import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # Calcola la directory base del progetto risalendo di tre livelli
DB_PATH = os.path.join(BASE_DIR, "instance", "database.db") # Percorso assoluto al database SQLite

def get_connection(): # Crea una connessione SQLite con foreign keys attive e righe accessibili come dict
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def query_one(query, params=()): # Esegue una SELECT e restituisce una sola riga (o None)
    with get_connection() as conn:
        cur = conn.execute(query, params)
        return cur.fetchone()

def query_all(query, params=()): # Esegue una SELECT e restituisce tutte le righe
    with get_connection() as conn:
        cur = conn.execute(query, params)
        return cur.fetchall()

def execute(query, params=()): # Esegue una query di modifica e restituisce l'ID dell'ultima riga inserita
    with get_connection() as conn:
        cur = conn.execute(query, params)
        conn.commit()
        return cur.lastrowid

def executemany(query, params_list): # Esegue la stessa query su più set di parametri e restituisce il numero di righe interessate
    with get_connection() as conn:
        cur = conn.executemany(query, params_list)
        conn.commit()
        return cur.rowcount