from app.bonus.repository import (
    get_registration_bonus,
    activate_user_bonus,
)
from app.database.db import execute, query_one


def activate_registration_bonus(user_id: int, method: str) -> dict:
    """
    Attiva il bonus di registrazione (classic | spid)
    """

    if method not in ("classic", "spid"):
        return {
            "success": False,
            "reason": "not_available",
            "new_balance": None,
        }

    # 🔒 se già attivato un bonus di registrazione → STOP
    existing = query_one(
        """
        SELECT 1
        FROM user_bonuses ub
        JOIN bonuses b ON b.id = ub.bonus_id
        WHERE ub.user_id = ?
          AND b.type = 'registration'
          AND ub.is_activated = 1
        """,
        (user_id,),
    )

    if existing:
        return {
            "success": False,
            "reason": "already_claimed",
            "new_balance": None,
        }

    bonus = get_registration_bonus(method)
    if not bonus:
        return {
            "success": False,
            "reason": "not_available",
            "new_balance": None,
        }

    bonus_id = bonus["id"]

    # ✅ assegna bonus (NON attivo)
    execute(
        """
        INSERT OR IGNORE INTO user_bonuses (user_id, bonus_id)
        VALUES (?, ?)
        """,
        (user_id, bonus_id),
    )

    # ✅ attiva bonus + accredito + log
    new_balance = activate_user_bonus(user_id, bonus_id)

    if new_balance is None:
        return {
            "success": False,
            "reason": "already_claimed",
            "new_balance": None,
        }

    return {
        "success": True,
        "reason": None,
        "new_balance": new_balance,
    }