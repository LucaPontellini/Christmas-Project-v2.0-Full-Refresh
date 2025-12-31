from app.database.db import query_one, query_all, execute


def get_registration_bonus(method):
    return query_one(
        """
        SELECT *
        FROM bonuses
        WHERE type = 'registration'
          AND method = ?
          AND is_active = 1
        """,
        (method,),
    )


def get_user_bonuses(user_id):
    """
    Ritorna SOLO i bonus dell’utente
    (niente bonus globali inutili)
    """
    return query_all(
        """
        SELECT
            b.id AS bonus_id,
            b.type,
            b.method,
            b.amount,
            ub.is_activated,
            ub.activated_at
        FROM user_bonuses ub
        JOIN bonuses b ON b.id = ub.bonus_id
        WHERE ub.user_id = ?
        """,
        (user_id,),
    )


def activate_user_bonus(user_id: int, bonus_id: int) -> int | None:
    """
    Attiva un bonus UNA SOLA VOLTA
    - se già attivo → None
    - se attivato → accredita saldo + log
    """

    # 1️⃣ attiva bonus (solo se NON attivo)
    updated_rows = execute(
        """
        UPDATE user_bonuses
        SET is_activated = 1,
            activated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
          AND bonus_id = ?
          AND is_activated = 0
        """,
        (user_id, bonus_id),
    )
    
    if updated_rows == 0:
        return None

    # 2️⃣ accredita saldo
    execute(
        """
        UPDATE users
        SET balance = balance + (
            SELECT amount FROM bonuses WHERE id = ?
        )
        WHERE id = ?
        """,
        (bonus_id, user_id),
    )

    # 3️⃣ log transazione (BONUS)
    execute(
        """
        INSERT INTO transactions (user_id, type, amount)
        VALUES (
            ?,
            'bonus',
            (SELECT amount FROM bonuses WHERE id = ?)
        )
        """,
        (user_id, bonus_id),
    )

    # 4️⃣ ritorna saldo aggiornato
    row = query_one(
        "SELECT balance FROM users WHERE id = ?",
        (user_id,),
    )

    return row["balance"]