from app.database.db import query_one, execute


def create_user(username, password, avatar, role="user"):
    return execute("""
        INSERT INTO users (username, password, avatar, role)
        VALUES (?, ?, ?, ?)
    """, (username, password, avatar, role))


def get_user_by_username(username):
    return query_one(
        "SELECT * FROM users WHERE username = ? AND is_deleted = 0",
        (username,)
    )

def get_user_by_id(user_id):
    return query_one(
        "SELECT * FROM users WHERE id = ? AND is_deleted = 0",
        (user_id,)
    )

# Aggiungi questa funzione nel repository dell'account
def get_user_by_username_any(username):
    """Recupera l'utente per username ignorando se è cancellato o meno"""
    return query_one("SELECT * FROM users WHERE username = ?", (username,))

# Assicurati che ci sia anche questa (servirà alla rotta admin)
def get_user_by_id_any(user_id):
    """Recupera l'utente per ID ignorando se è cancellato o meno"""
    return query_one("SELECT * FROM users WHERE id = ?", (user_id,))

def update_password(user_id, hashed_password):
    execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (hashed_password, user_id)
    )

# Rimuovi o correggi questa se la usi ancora
def save_pin(user_id, pin, expires_at):
    execute("""
        INSERT INTO password_reset_pins (user_id, pin, expires_at)
        VALUES (?, ?, ?)
    """, (user_id, pin, expires_at))

def save_reset_pin(user_id, pin, expires_at):
    """Salva il PIN di reset (Uniformata su password_reset_pins)"""
    execute("""
        INSERT INTO password_reset_pins (user_id, pin, expires_at)
        VALUES (?, ?, ?)
    """, (user_id, pin, expires_at))

def verify_pin(user_id, pin):
    """Verifica se il PIN è corretto e non scaduto"""
    row = query_one("""
        SELECT 1 FROM password_reset_pins
        WHERE user_id = ? AND pin = ? 
        AND expires_at > CURRENT_TIMESTAMP
    """, (user_id, pin))
    return row is not None

def delete_pins_for_user(user_id):
    """Pulisce i PIN usati o vecchi"""
    execute("DELETE FROM password_reset_pins WHERE user_id = ?", (user_id,))

def update_password(user_id, hashed_password):
    execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))

def soft_delete_user(user_id):
    execute("""
        UPDATE users
        SET is_deleted = 1,
            deleted_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (user_id,))


def hard_delete_user(user_id):
    # Il nome corretto della tabella è password_reset_pins
    execute("DELETE FROM password_reset_pins WHERE user_id = ?", (user_id,))
    execute("DELETE FROM access_logs WHERE user_id = ?", (user_id,))
    execute("DELETE FROM user_bonuses WHERE user_id = ?", (user_id,))
    execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
    
    # Per i log admin, l'utente può essere sia l'autore (admin_id) che il bersaglio (target_user_id)
    execute("DELETE FROM admin_logs WHERE admin_id = ? OR target_user_id = ?", (user_id, user_id))
    
    # Infine elimina l'utente
    execute("DELETE FROM users WHERE id = ?", (user_id,))


def add_balance(user_id, amount):
    execute("""
        UPDATE users
        SET balance = balance + ?
        WHERE id = ?
    """, (amount, user_id))


def create_transaction(user_id, amount, type_):
    execute("""
        INSERT INTO transactions (user_id, amount, type)
        VALUES (?, ?, ?)
    """, (user_id, amount, type_))