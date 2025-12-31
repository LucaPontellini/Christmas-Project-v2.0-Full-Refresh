from flask import Blueprint, render_template, redirect, url_for, session, flash

from app.account.repository import get_user_by_id
from app.bonus.repository import get_user_bonuses, get_registration_bonus
from app.utils.color import get_user_color, get_user_initial

casino = Blueprint("casino", __name__, url_prefix="/casino")


# ---------------------------
# LOBBY
# ---------------------------
@casino.route("/")
def lobby():
    user = None
    user_color = None
    user_initial = None

    registration_bonuses = {
        "spid": {
            "available": False,
            "amount": 0,
            "claimed": False,
        },
        "classic": {
            "available": False,
            "amount": 0,
            "claimed": False,
        },
    }

    if "user_id" in session:
        user = get_user_by_id(session["user_id"])

        # sessione sporca → reset
        if not user:
            session.clear()
            return redirect(url_for("casino.lobby"))
        
        user_color = get_user_color(user["username"])
        user_initial = get_user_initial(user["username"])

        # 🔒 ADMIN: niente bonus
        if user["role"] != "admin":

            user_bonuses = get_user_bonuses(user["id"])

            # solo bonus ATTIVATI
            claimed_types = {
                b["method"]
                for b in user_bonuses
                if b["is_activated"]
            }

            # ---------------------------
            # SPID
            # ---------------------------
            spid_bonus = get_registration_bonus("spid")
            if spid_bonus:
                registration_bonuses["spid"]["available"] = True
                registration_bonuses["spid"]["amount"] = spid_bonus["amount"]
                registration_bonuses["spid"]["claimed"] = "spid" in claimed_types

            # ---------------------------
            # CLASSIC
            # ---------------------------
            classic_bonus = get_registration_bonus("classic")
            if classic_bonus:
                registration_bonuses["classic"]["available"] = True
                registration_bonuses["classic"]["amount"] = classic_bonus["amount"]
                registration_bonuses["classic"]["claimed"] = "classic" in claimed_types

    return render_template(
        "casino/lobby.html",
        user=user,
        user_color=user_color,
        user_initial=user_initial,
        registration_bonuses=registration_bonuses,
    )


# ---------------------------
# PLAY (PLACEHOLDER)
# ---------------------------
@casino.route("/play")
def play():
    if "user_id" not in session:
        return redirect(url_for("casino.lobby", open="login"))

    flash("La sezione giochi non è ancora disponibile.", "info")
    return redirect(url_for("casino.lobby"))


@casino.route("/play/<game>")
def play_game(game):
    if "user_id" not in session:
        return redirect(url_for("casino.lobby", open="login"))

    flash("Questo gioco non è ancora disponibile.", "info")
    return redirect(url_for("casino.lobby"))


# ---------------------------
# CASHIER (DISABILITATO)
# ---------------------------
@casino.route("/cashier")
def cashier():
    if "user_id" not in session:
        return redirect(url_for("casino.lobby", open="login"))

    flash("La sezione cassiere non è ancora disponibile.", "info")
    return redirect(url_for("casino.lobby"))