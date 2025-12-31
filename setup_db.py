import sqlite3
from werkzeug.security import generate_password_hash
import os

# Percorsi base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(DB_DIR, "database.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "app", "database", "schema.sql")


def setup_database():
    os.makedirs(DB_DIR, exist_ok=True)

    first_creation = not os.path.exists(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Creazione tabelle (solo se DB nuovo)
    if first_creation:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cur.executescript(f.read())

    # Creazione admin di default
    cur.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO users (username, password, avatar, role)
            VALUES (?, ?, ?, ?)
        """, (
            "admin",
            generate_password_hash("admin123"),
            "images/Luca_Pontellini.jpg",
            "admin"
        ))

    conn.commit()
    conn.close()
    print("Database pronto")


if __name__ == "__main__":
    setup_database()