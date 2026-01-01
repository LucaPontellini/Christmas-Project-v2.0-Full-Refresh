from flask import Blueprint, request, session, jsonify

from app.bonus.services import activate_registration_bonus
from app.account.repository import get_user_by_id

bonus_bp = Blueprint("bonus", __name__, url_prefix="/bonus") # Blueprint per le rotte relative ai bonus

@bonus_bp.route("/claim", methods=["POST"]) # Rotta per richiedere il bonus di registrazione
def claim_bonus():

    # Verifica autenticazione tramite sessione
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "error": "Not authenticated"
        }), 401

    # La richiesta deve essere JSON
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Invalid request"
        }), 400

    # Recupero utente dal DB
    user_id = session["user_id"]
    user = get_user_by_id(user_id)

    # Utente inesistente
    if not user:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    # Gli admin non possono richiedere bonus
    if user["role"] == "admin":
        return jsonify({
            "success": False,
            "error": "Admins cannot claim bonuses"
        }), 403

    # Utente disabilitato (soft delete)
    if user["is_deleted"]:
        return jsonify({
            "success": False,
            "error": "User disabled"
        }), 403

    # Parsing del JSON e validazione del metodo
    data = request.get_json()
    method = data.get("method")

    # Metodo non valido
    if method not in ("classic", "spid"):
        return jsonify({
            "success": False,
            "error": "Invalid method"
        }), 400

    # Attivazione del bonus tramite servizio
    result = activate_registration_bonus(user_id, method)

    # Gestione errori dal servizio
    if not result["success"]:
        if result["reason"] == "already_claimed":
            return jsonify({
                "success": False,
                "error": "Bonus already claimed"
            }), 409

        return jsonify({
            "success": False,
            "error": "Bonus not available"
        }), 400

    # Risposta in caso di successo
    return jsonify({
        "success": True,
        "new_balance": result["new_balance"]
    }), 200