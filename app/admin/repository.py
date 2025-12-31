from app.database.db import query_one, query_all, execute

# --- STATISTICHE ---
def get_dashboard_stats():
    users_res = query_one("SELECT COUNT(*) AS total FROM users WHERE is_deleted = 0")
    deleted_res = query_one("SELECT COUNT(*) AS total FROM users WHERE is_deleted = 1")
    
    chips_res = query_one("""
        SELECT SUM(uc.amount * cc.value) AS total 
        FROM user_chips uc 
        JOIN chip_colors cc ON uc.color_id = cc.id
    """)
    
    # Calcolo GGR corretto
    finance_res = query_one("""
        SELECT 
            SUM(CASE WHEN type = 'perdita' THEN amount ELSE 0 END) AS perdite,
            SUM(CASE WHEN type = 'vincita' THEN amount ELSE 0 END) AS vincite,
            SUM(CASE WHEN type = 'bonus' THEN amount ELSE 0 END) AS total_bonuses
        FROM transactions
    """)

    val_perdite = finance_res["perdite"] or 0
    val_vincite = finance_res["vincite"] or 0
    
    return {
        "users": users_res["total"] or 0,
        "deleted": deleted_res["total"] or 0,
        "total_chips_value": chips_res["total"] or 0,
        "revenue": val_perdite - val_vincite,
        "total_bonuses": finance_res["total_bonuses"] or 0
    }

# --- LISTE ---
def get_all_users(include_deleted=True):
    sql = "SELECT id, username, balance, is_deleted, created_at FROM users"
    if not include_deleted:
        sql += " WHERE is_deleted = 0"
    return query_all(sql + " ORDER BY created_at DESC")

def get_recent_transactions(limit=10):
    return query_all("""
        SELECT t.*, u.username FROM transactions t 
        JOIN users u ON t.user_id = u.id 
        ORDER BY t.created_at DESC LIMIT ?
    """, (limit,))

def get_access_logs(limit=10):
    return query_all("""
        SELECT a.*, u.username FROM access_logs a 
        LEFT JOIN users u ON u.id = a.user_id 
        ORDER BY a.created_at DESC LIMIT ?
    """, (limit,))

# --- AZIONI ---
def soft_delete_user(user_id):
    execute("UPDATE users SET is_deleted = 1, deleted_at = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))

# Aggiungi questa funzione per eliminare fisicamente l'utente
def hard_delete_user(user_id):
    # 1. Eliminiamo i log amministrativi collegati a questo utente per evitare errori di vincolo
    execute("DELETE FROM admin_logs WHERE target_user_id = ?", (user_id,))
    # 2. Eliminiamo i log degli accessi
    execute("DELETE FROM access_logs WHERE user_id = ?", (user_id,))
    # 3. Eliminiamo le transazioni
    execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
    # 4. Infine eliminiamo l'utente
    execute("DELETE FROM users WHERE id = ?", (user_id,))

def restore_user(user_id):
    execute("UPDATE users SET is_deleted = 0, deleted_at = NULL WHERE id = ?", (user_id,))

def update_user_balance_admin(user_id, amount, reason):
    execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
    tx_type = 'manual_adj' if reason == 'adjustment' else 'bonus'
    execute("INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)", (user_id, tx_type, amount))

def get_all_bonuses():
    return query_all("SELECT * FROM bonuses ORDER BY created_at DESC")

def update_user_balance(user_id, new_balance):
    execute(
        "UPDATE users SET balance = ? WHERE id = ?",
        (new_balance, user_id)
    )

def restore_user(user_id):
    execute("""
        UPDATE users
        SET is_deleted = 0,
            deleted_at = NULL
        WHERE id = ?
    """, (user_id,))

def log_admin_action(admin_id, target_user_id, action):
    execute("""
        INSERT INTO admin_logs (admin_id, target_user_id, action)
        VALUES (?, ?, ?)
    """, (admin_id, target_user_id, action))

def get_admin_logs(limit=20):
    return query_all("""
        SELECT 
            l.*,
            a.username AS admin_username,
            u.username AS target_username
        FROM admin_logs l
        JOIN users a ON a.id = l.admin_id
        JOIN users u ON u.id = l.target_user_id
        ORDER BY l.created_at DESC
        LIMIT ?
    """, (limit,))