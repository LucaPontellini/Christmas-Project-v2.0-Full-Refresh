from app.bonus.repository import get_registration_bonus, activate_user_bonus
from app.database.db import execute, query_one

def activate_registration_bonus(user_id: int, method: str) -> dict: # attiva bonus di registrazione per l’utente

    # valida metodo bonus (solo classic | spid)
    if method not in ("classic", "spid"):
        return {
            "success": False,
            "reason": "not_available",
            "new_balance": None,
        }

    # verifica se l’utente ha già un bonus di registrazione attivato
    existing = query_one(
        """ SELECT 1
        FROM user_bonuses ub
        JOIN bonuses b ON b.id = ub.bonus_id
        WHERE ub.user_id = ?
          AND b.type = 'registration'
          AND ub.is_activated = 1
        """, (user_id,),
    )

    # se già attivato → blocca
    if existing:
        return {
            "success": False,
            "reason": "already_claimed",
            "new_balance": None,
        }

    # recupera il bonus di registrazione per il metodo richiesto
    bonus = get_registration_bonus(method)
    if not bonus:
        return {
            "success": False,
            "reason": "not_available",
            "new_balance": None,
        }

    bonus_id = bonus["id"]

    # assegna il bonus all’utente (in stato non attivo)
    execute(
        """INSERT OR IGNORE INTO user_bonuses (user_id, bonus_id)
        VALUES (?, ?) """, (user_id, bonus_id),
    )

    # attiva il bonus: accredito + update stato + log
    new_balance = activate_user_bonus(user_id, bonus_id)

    # se l’attivazione fallisce (es. già attivo) --> blocca
    if new_balance is None:
        return {
            "success": False,
            "reason": "already_claimed",
            "new_balance": None,
        }

    # attivazione riuscita
    return {
        "success": True,
        "reason": None,
        "new_balance": new_balance,
    }