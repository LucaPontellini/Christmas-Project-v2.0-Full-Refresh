from flask import Blueprint, request, session, jsonify

from app.bonus.services import activate_registration_bonus
from app.account.repository import get_user_by_id

bonus_bp = Blueprint("bonus", __name__, url_prefix="/bonus")


@bonus_bp.route("/claim", methods=["POST"])
def claim_bonus():

    # ---------------------------
    # AUTH CHECK
    # ---------------------------
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "error": "Not authenticated"
        }), 401

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Invalid request"
        }), 400

    user_id = session["user_id"]
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    if user["role"] == "admin":
        return jsonify({
            "success": False,
            "error": "Admins cannot claim bonuses"
        }), 403
    
    if user["is_deleted"]:
        return jsonify({
            "success": False,
            "error": "User disabled"
        }), 403

    # ---------------------------
    # REQUEST DATA
    # ---------------------------
    data = request.get_json()
    method = data.get("method")

    if method not in ("classic", "spid"):
        return jsonify({
            "success": False,
            "error": "Invalid method"
        }), 400

    # ---------------------------
    # BONUS ACTIVATION
    # ---------------------------
    result = activate_registration_bonus(user_id, method)

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

    # ---------------------------
    # SUCCESS RESPONSE
    # ---------------------------
    return jsonify({
        "success": True,
        "new_balance": result["new_balance"]
    }), 200