from app.database.db import query_one, query_all, execute

def get_registration_bonus(method):
    # Recupera il bonus di registrazione attivo per un determinato metodo
    return query_one(
        """SELECT * FROM bonuses 
           WHERE type = 'registration' AND method = ? AND is_active = 1""", (method,)
    )

def get_user_bonuses(user_id):
    # Restituisce solo i bonus associati all’utente
    return query_all(
        """SELECT 
                b.id AS bonus_id,
                b.type,
                b.method,
                b.amount,
                ub.is_activated,
                ub.activated_at
           FROM user_bonuses ub
           JOIN bonuses b ON b.id = ub.bonus_id
           WHERE ub.user_id = ?""",
        (user_id,)
    )

def activate_user_bonus(user_id: int, bonus_id: int) -> int | None:
    # Prova ad attivare il bonus (solo se non già attivo)
    updated_rows = execute(
        """UPDATE user_bonuses
           SET is_activated = 1,
               activated_at = CURRENT_TIMESTAMP
           WHERE user_id = ? AND bonus_id = ? AND is_activated = 0""",
        (user_id, bonus_id)
    )

    # Nessuna riga aggiornata --> bonus già attivo o non valido
    if updated_rows == 0:
        return None

    # Accredita l’importo del bonus al saldo dell’utente
    execute(
        """UPDATE users
           SET balance = balance + (SELECT amount FROM bonuses WHERE id = ?)
           WHERE id = ?""", (bonus_id, user_id)
    )

    # Registra la transazione come bonus
    execute(
        """INSERT INTO transactions (user_id, type, amount)
           VALUES (?, 'bonus', (SELECT amount FROM bonuses WHERE id = ?))""", (user_id, bonus_id)
    )

    # Ritorna il saldo aggiornato
    row = query_one("SELECT balance FROM users WHERE id = ?", (user_id,))

    return row["balance"]