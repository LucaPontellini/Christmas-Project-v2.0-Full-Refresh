import sqlite3
from werkzeug.security import generate_password_hash
import os

# Percorsi base del progetto
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Directory principale del progetto
DB_DIR = os.path.join(BASE_DIR, "instance") # Cartella che conterrà il database
DB_PATH = os.path.join(DB_DIR, "database.db") # Percorso completo al file SQLite
SCHEMA_PATH = os.path.join(BASE_DIR, "app", "database", "schema.sql") # File SQL con la definizione delle tabelle

def setup_database():
    os.makedirs(DB_DIR, exist_ok=True) # Crea la cartella "instance" se non esiste

    first_creation = not os.path.exists(DB_PATH) # Verifica se il database esiste già

    # Connessione al database SQLite
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Se il DB è nuovo, esegue lo schema SQL per creare le tabelle
    if first_creation:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cur.executescript(f.read())

    # Creazione dell'utente admin di default (solo se non esiste già)
    cur.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    if not cur.fetchone():
        cur.execute(
            """INSERT INTO users (username, password, avatar, role)
               VALUES (?, ?, ?, ?)""",
            ("admin", generate_password_hash("admin123"), # Password hashata
             "images/Luca_Pontellini.jpg", # Avatar di default
                "admin" # Ruolo amministratore
            ))

    # Salva le modifiche e chiude la connessione
    conn.commit()
    conn.close()

    print("Database pronto")

if __name__ == "__main__":
    setup_database()