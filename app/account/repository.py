from app.database.db import query_one, execute

# Crea un nuovo utente nel database
def create_user(username, password, avatar, role="user"):
    return execute("""
        INSERT INTO users (username, password, avatar, role)
        VALUES (?, ?, ?, ?)
    """, (username, password, avatar, role))

# Recupera un utente attivo (non soft-deleted) tramite username
def get_user_by_username(username):
    return query_one(
        "SELECT * FROM users WHERE username = ? AND is_deleted = 0",
        (username,)
    )

# Recupera un utente attivo tramite ID
def get_user_by_id(user_id):
    return query_one(
        "SELECT * FROM users WHERE id = ? AND is_deleted = 0",
        (user_id,)
    )

# Recupera un utente tramite username ignorando lo stato di cancellazione
def get_user_by_username_any(username):
    return query_one("SELECT * FROM users WHERE username = ?", (username,))

# Recupera un utente tramite ID ignorando lo stato di cancellazione
def get_user_by_id_any(user_id):
    return query_one("SELECT * FROM users WHERE id = ?", (user_id,))

# Aggiorna la password dell’utente
def update_password(user_id, hashed_password):
    execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (hashed_password, user_id)
    )

# Salva un PIN di reset password con scadenza
def save_pin(user_id, pin, expires_at):
    execute("""
        INSERT INTO password_reset_pins (user_id, pin, expires_at)
        VALUES (?, ?, ?)
    """, (user_id, pin, expires_at))

# Alias della funzione precedente (uniformato al naming)
def save_reset_pin(user_id, pin, expires_at):
    execute("""
        INSERT INTO password_reset_pins (user_id, pin, expires_at)
        VALUES (?, ?, ?)
    """, (user_id, pin, expires_at))

# Verifica che il PIN esista e non sia scaduto
def verify_pin(user_id, pin):
    row = query_one("""
        SELECT 1 FROM password_reset_pins
        WHERE user_id = ? AND pin = ? 
        AND expires_at > CURRENT_TIMESTAMP
    """, (user_id, pin))
    return row is not None

# Elimina tutti i PIN associati all’utente (vecchi o usati)
def delete_pins_for_user(user_id):
    execute("DELETE FROM password_reset_pins WHERE user_id = ?", (user_id,))

# Aggiorna la password dell’utente (duplicato della funzione sopra)
def update_password(user_id, hashed_password):
    execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))

# Soft delete: disattiva l’utente mantenendo i dati
def soft_delete_user(user_id):
    execute("""
        UPDATE users
        SET is_deleted = 1,
            deleted_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (user_id,))

# Hard delete: rimuove completamente l’utente e tutte le sue relazioni dal database
def hard_delete_user(user_id):
    execute("DELETE FROM password_reset_pins WHERE user_id = ?", (user_id,))
    execute("DELETE FROM access_logs WHERE user_id = ?", (user_id,))
    execute("DELETE FROM user_bonuses WHERE user_id = ?", (user_id,))
    execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
    
    # Rimuove i log admin dove l’utente è autore o bersaglio
    execute("DELETE FROM admin_logs WHERE admin_id = ? OR target_user_id = ?", (user_id, user_id))
    
    # Elimina definitivamente l’utente
    execute("DELETE FROM users WHERE id = ?", (user_id,))

# Aggiunge saldo al conto dell’utente
def add_balance(user_id, amount):
    execute("""
        UPDATE users
        SET balance = balance + ?
        WHERE id = ?
    """, (amount, user_id))

# Registra una transazione (deposito, prelievo, bonus, ecc.)
def create_transaction(user_id, amount, type_):
    execute("""
        INSERT INTO transactions (user_id, amount, type)
        VALUES (?, ?, ?)
    """, (user_id, amount, type_))