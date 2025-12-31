from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.account.repository import (
    get_user_by_username,
    get_user_by_id,
    create_user,
    get_user_by_username_any,
    update_password,
    verify_pin,
    delete_pins_for_user,
    soft_delete_user,
)

from app.account.services import create_reset_pin
from app.bonus.repository import get_registration_bonus
from app.database.db import execute, query_one

account = Blueprint("account", __name__, url_prefix="/account")

# ---------------------------
# REGISTRAZIONE
# ---------------------------
@account.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Missing required fields", "register_error")
        return redirect(url_for("casino.lobby", open="register"))

    if len(password) < 6:
        flash("Password must be at least 6 characters", "register_error")
        return redirect(url_for("casino.lobby", open="register"))

    existing = get_user_by_username_any(username)

    if existing:
        if existing["is_deleted"]:
            flash(
                "This username was previously used and is disabled. Please contact support.",
                "register_error"
            )
        else:
            flash(
                "This username already exists. Please log in.",
                "register_error"
            )
        return redirect(url_for("casino.lobby", open="register"))

    create_user(
        username=username,
        password=generate_password_hash(password),
        avatar="images/user_icon.png",
        role="user",
    )

    flash("Registration completed! Login now.", "success")
    return redirect(url_for("casino.lobby", open="login"))

# ---------------------------
# LOGIN
# ---------------------------
@account.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    auth_method = request.form.get("auth_method", "standard")

    user = get_user_by_username(username)

    if not user or not check_password_hash(user["password"], password):
        flash("Incorrect username or password. Please try again.", "login_error")
        return redirect(url_for("casino.lobby", open="login"))

    session.clear()
    session["user_id"] = user["id"]
    session["role"] = user["role"]

    # Gestione Bonus (solo per utenti non admin)
    if user["role"] != "admin":
        bonus_already_claimed = query_one(
            "SELECT 1 FROM user_bonuses WHERE user_id = ?",
            (user["id"],),
        )

        if not bonus_already_claimed:
            bonus_type = "spid" if auth_method == "spid" else "classic"
            bonus_data = get_registration_bonus(bonus_type)

            if bonus_data:
                execute(
                    "INSERT INTO user_bonuses (user_id, bonus_id) VALUES (?, ?)",
                    (user["id"], bonus_data["id"]),
                )
                execute(
                    "UPDATE users SET balance = balance + ? WHERE id = ?",
                    (bonus_data["amount"], user["id"]),
                )
                flash(
                    f"You received a {bonus_data['amount']}€ {bonus_type.upper()} bonus!",
                    "success",
                )

    execute(
        "INSERT INTO access_logs (user_id, action, ip_address) VALUES (?, 'login', ?)",
        (user["id"], request.remote_addr),
    )

    flash(f"Welcome back, {user['username']}!", "success")
    return redirect(url_for("casino.lobby"))

# ---------------------------
# LOGOUT
# ---------------------------
@account.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("casino.lobby"))

# ---------------------------
# FORGOT PASSWORD → GENERA PIN
# ---------------------------
@account.route("/forgot-pin", methods=["POST"])
def forgot_pin():
    username = request.form.get("username")

    if not username:
        flash("Username required", "forgot_error")
        return redirect(url_for("casino.lobby", open="forgot"))

    user = get_user_by_username(username)
    if not user:
        flash("No account found with that username", "forgot_error")
        return redirect(url_for("casino.lobby", open="forgot"))

    # Genera il PIN tramite il service e salva in sessione l'username per il reset
    pin = create_reset_pin(user["id"])
    session["reset_username"] = username

    # Passiamo il PIN via flash (categoria 'reset_pin') per attivare il modal in JS
    flash(pin, "reset_pin")

    return redirect(url_for("casino.lobby"))

# ---------------------------
# RESET PASSWORD
# ---------------------------
@account.route("/reset-password", methods=["POST"])
def reset_password():
    username = request.form.get("username")
    pin = request.form.get("pin")
    new_password = request.form.get("password")

    # Validazione dati
    if not username or not pin or not new_password:
        flash("Missing data", "reset_error")
        return redirect(url_for("casino.lobby"))

    if session.get("reset_username") != username:
        flash("Session expired. Try again.", "reset_error")
        return redirect(url_for("casino.lobby"))

    user = get_user_by_username(username)
    if not user:
        flash("Invalid user", "reset_error")
        return redirect(url_for("casino.lobby"))

    # Verifica se il PIN inserito è corretto
    if verify_pin(user["id"], pin):
        # CASO 1: PIN CORRETTO
        update_password(user["id"], generate_password_hash(new_password))
        delete_pins_for_user(user["id"])
        session.pop("reset_username", None)
        flash("Password updated! Log in now.", "success")
        return redirect(url_for("casino.lobby", open="login"))
    else:
        # CASO 2: PIN ERRATO -> RIGENERAZIONE AUTOMATICA
        # Usiamo la tua funzione per creare un nuovo codice
        new_pin_code = create_reset_pin(user["id"])
        
        # Inviamo entrambi i messaggi flash
        flash("Invalid PIN. A new one has been generated for you.", "reset_error")
        flash(new_pin_code, "reset_pin") 
        
        # Il redirect ricarica la pagina:
        # - reset_error apre il modal tramite JS
        # - reset_pin mostra il nuovo box dorato
        return redirect(url_for("casino.lobby"))

# ---------------------------
# DELETE ACCOUNT (SOFT)
# ---------------------------
@account.route("/delete", methods=["POST"])
def delete_account():
    if "user_id" not in session:
        abort(403)

    user = get_user_by_id(session["user_id"])
    if not user:
        abort(404)

    if user["role"] == "admin":
        abort(403)

    soft_delete_user(user["id"])
    session.clear()

    flash("Your account has been deleted.", "info")
    return redirect(url_for("casino.lobby"))