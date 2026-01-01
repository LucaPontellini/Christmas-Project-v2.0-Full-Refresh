from datetime import datetime
from app.database.db import query_one, query_all, execute

# --- STATISTICHE DASHBOARD ---
def get_dashboard_stats():
    # Recupera numero utenti attivi
    users_res = query_one("SELECT COUNT(*) AS total FROM users WHERE is_deleted = 0")
    
    # Recupera numero utenti eliminati
    deleted_res = query_one("SELECT COUNT(*) AS total FROM users WHERE is_deleted = 1")
    
    # Calcola valore totale delle chips in circolazione
    chips_res = query_one("""
        SELECT SUM(uc.amount * cc.value) AS total 
        FROM user_chips uc 
        JOIN chip_colors cc ON uc.color_id = cc.id
    """)

    # Calcola statistiche finanziarie (perdite, vincite, bonus)
    finance_res = query_one("""
        SELECT 
            SUM(CASE WHEN type = 'perdita' THEN amount ELSE 0 END) AS perdite,
            SUM(CASE WHEN type = 'vincita' THEN amount ELSE 0 END) AS vincite,
            SUM(CASE WHEN type = 'bonus' THEN amount ELSE 0 END) AS total_bonuses
        FROM transactions
    """)

    # Gestione dei valori NULL (se il database è vuoto mette 0)
    val_perdite = finance_res["perdite"] or 0
    val_vincite = finance_res["vincite"] or 0

    return {
        "users": users_res["total"] or 0,
        "deleted": deleted_res["total"] or 0,
        "total_chips_value": chips_res["total"] or 0,
        "revenue": val_perdite - val_vincite,
        "total_bonuses": finance_res["total_bonuses"] or 0
    }

# --- LISTE UTENTI E TRANSAZIONI ---
def get_all_users(include_deleted=True):
    sql = "SELECT id, username, balance, is_deleted, created_at, role FROM users"
    if not include_deleted:
        sql += " WHERE is_deleted = 0"
    return query_all(sql + " ORDER BY created_at DESC")

def get_recent_transactions(limit=100):
    return query_all("""
        SELECT t.*, u.username 
        FROM transactions t 
        JOIN users u ON t.user_id = u.id 
        ORDER BY t.created_at DESC 
        LIMIT ?
    """, (limit,))

# --- LOG DI ACCESSO E ADMIN ---
def get_access_logs(limit=100):
    return query_all("""
        SELECT a.user_id, a.action, a.created_at, u.username 
        FROM access_logs a 
        LEFT JOIN users u ON u.id = a.user_id 
        ORDER BY a.created_at DESC 
        LIMIT ?
    """, (limit,))

def get_admin_logs(limit=100):
    # Log azioni admin o sicurezza (dalla tabella admin_logs)
    return query_all("""
        SELECT l.target_user_id AS user_id, l.action, l.created_at, u.username 
        FROM admin_logs l
        LEFT JOIN users u ON u.id = l.target_user_id
        ORDER BY l.created_at DESC
        LIMIT ?
    """, (limit,))

def get_system_activity(limit=100):
    # Recuperiamo entrambi i tipi di log
    logs_accesso = get_access_logs(limit)
    logs_admin = get_admin_logs(limit)
    
    # Li uniamo in una lista sola
    tutti_i_logs = logs_accesso + logs_admin
    
    # Li ordiniamo per data (la X nel comando sotto dice a Python di guardare 'created_at')
    # Usiamo str() per essere sicuri che il confronto tra date funzioni sempre
    tutti_i_logs.sort(key=lambda x: str(x['created_at']), reverse=True)
    
    # Restituiamo solo i primi risultati richiesti
    return tutti_i_logs[:limit]

# --- AZIONI DI GESTIONE ---
def log_admin_action(admin_id, target_user_id, action):
    execute("""
        INSERT INTO admin_logs (admin_id, target_user_id, action, created_at)
        VALUES (?, ?, ?, ?)
    """, (admin_id, target_user_id, action, datetime.now())) # Ora locale

def soft_delete_user(user_id):
    execute("UPDATE users SET is_deleted = 1, deleted_at = ? WHERE id = ?", (datetime.now(), user_id))

def hard_delete_user(user_id):
    execute("DELETE FROM admin_logs WHERE target_user_id = ?", (user_id,))
    execute("DELETE FROM access_logs WHERE user_id = ?", (user_id,))
    execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
    execute("DELETE FROM users WHERE id = ?", (user_id,))

def restore_user(user_id):
    execute("UPDATE users SET is_deleted = 0, deleted_at = NULL WHERE id = ?", (user_id,))

def update_user_balance_admin(user_id, amount, reason):
    # Aggiornamento saldo dell'utente
    execute(
        "UPDATE users SET balance = balance + ? WHERE id = ?", 
        (amount, user_id)
    )
    
    # Definizione tipo transazione
    if reason == 'adjustment':
        tx_type = 'manual_adj'
    else: tx_type = 'bonus'
    
    # Inserimento log transazione con ora locale
    query = """INSERT INTO transactions (user_id, type, amount, created_at) VALUES (?, ?, ?, ?)"""
    
    params = (user_id, tx_type, amount, datetime.now())
    
    execute(query, params)

def get_all_bonuses():
    return query_all("SELECT * FROM bonuses ORDER BY created_at DESC")