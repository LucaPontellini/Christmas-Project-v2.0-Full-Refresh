from flask import Blueprint, request, redirect, url_for, session, flash, abort
from werkzeug.security import check_password_hash, generate_password_hash

from app.account.repository import get_user_by_username, get_user_by_id, create_user, get_user_by_username_any, update_password, verify_pin, delete_pins_for_user, soft_delete_user
from app.account.services import create_reset_pin
from app.admin.repository import log_admin_action
from app.bonus.repository import get_registration_bonus
from app.database.db import execute, query_one

# Definisce il Blueprint per l'account
account = Blueprint("account", __name__, url_prefix="/account")

# Registrazione utente
@account.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    # Controllo se i campi sono vuoti
    if not username or not password:
        flash("Missing required fields", "register_error")
        return redirect(url_for("casino.lobby", open="register"))

    # Controllo lunghezza password
    if len(password) < 6:
        flash("Password must be at least 6 characters", "register_error")
        return redirect(url_for("casino.lobby", open="register"))

    # Controllo se l'username esiste già
    existing = get_user_by_username_any(username)
    if existing:
        if existing["is_deleted"]:
            flash("This username was previously used and is disabled.", "register_error")
        else:
            flash("This username already exists.", "register_error")
        return redirect(url_for("casino.lobby", open="register"))

    # Crea l'utente nel database
    password_hashata = generate_password_hash(password)
    create_user(username=username, password=password_hashata, avatar="images/user_icon.png", role="user")
    
    # Recupera l'utente appena creato per fargli il log
    nuovo_utente = get_user_by_username(username)
    if nuovo_utente:
        # Registra l'azione nella dashboard admin
        log_admin_action(None, nuovo_utente['id'], "registration")

    flash("Registration completed! Login now.", "success")
    return redirect(url_for("casino.lobby", open="login"))

# Login utente
@account.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    auth_method = request.form.get("auth_method", "standard")

    user = get_user_by_username(username)

    # Controlla se l'utente esiste e la password è giusta
    if not user:
        flash("User not found.", "login_error")
        return redirect(url_for("casino.lobby", open="login"))
    
    if not check_password_hash(user["password"], password):
        flash("Incorrect password.", "login_error")
        return redirect(url_for("casino.lobby", open="login"))

    # Pulisce la sessione vecchia e crea quella nuova
    session.clear()
    session["user_id"] = user["id"]
    session["role"] = user["role"]

    # Assegnazione del bonus di registrazione se applicabile
    if user["role"] != "admin":
        # Controlliamo se ha già preso bonus
        gia_preso = query_one("SELECT 1 FROM user_bonuses WHERE user_id = ?", (user["id"],))

        if not gia_preso:
            # Scegle se dare il bonus SPID o quello CLASSIC
            if auth_method == "spid":
                tipo_bonus = "spid"
            else:
                tipo_bonus = "classic"
            
            # Prende i dati del bonus (quanti soldi dare)
            dati_bonus = get_registration_bonus(tipo_bonus)

            if dati_bonus:
                # Dà il bonus all'utente
                execute("INSERT INTO user_bonuses (user_id, bonus_id) VALUES (?, ?)", (user["id"], dati_bonus["id"]))
                execute("UPDATE users SET balance = balance + ? WHERE id = ?", (dati_bonus["amount"], user["id"]))
                flash(f"You received a {dati_bonus['amount']}€ bonus!", "success")

    # Scrive il log per la Dashboard Admin (Tag Blu LOGIN)
    log_admin_action(None, user["id"], "login")

    flash(f"Welcome back, {user['username']}!", "success")
    return redirect(url_for("casino.lobby"))

# Logout utente
@account.route("/logout")
def logout():
    # Prende l'ID prima di cancellare la sessione
    id_utente = session.get("user_id")
    
    if id_utente:
        # Logga che è uscito
        log_admin_action(None, id_utente, "logout")

    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("casino.lobby"))

# Recupero password (FASE 1: GENERA PIN)
@account.route("/forgot-pin", methods=["POST"])
def forgot_pin():
    username = request.form.get("username")

    if not username:
        flash("Username required", "forgot_error")
        return redirect(url_for("casino.lobby", open="forgot"))

    user = get_user_by_username(username)
    if not user:
        flash("User not found.", "forgot_error")
        return redirect(url_for("casino.lobby", open="forgot"))

    # Crea il PIN e lo salva in sessione
    pin_generato = create_reset_pin(user["id"])
    session["reset_username"] = username

    # Logga la richiesta di sicurezza
    log_admin_action(None, user["id"], "pin_request")

    flash(pin_generato, "reset_pin")
    return redirect(url_for("casino.lobby"))

# Recupero password (FASE 2: NUOVA PASSWORD)
@account.route("/reset-password", methods=["POST"])
def reset_password():
    username = request.form.get("username")
    pin = request.form.get("pin")
    nuova_pass = request.form.get("password")

    # Controlli di sicurezza
    if not username or not pin or not nuova_pass:
        flash("Missing data", "reset_error")
        return redirect(url_for("casino.lobby"))

    user = get_user_by_username(username)
    
    # Verifica il PIN
    if verify_pin(user["id"], pin):
        # Se il PIN è giusto, cambia la password
        nuova_pass_hashata = generate_password_hash(nuova_pass)
        update_password(user["id"], nuova_pass_hashata)
        
        # Log di sicurezza
        log_admin_action(None, user["id"], "password_reset")
        
        # Pulizia PIN e sessione temporanea
        delete_pins_for_user(user["id"])
        session.pop("reset_username", None)
        
        flash("Password updated!", "success")
        return redirect(url_for("casino.lobby", open="login"))
    else:
        # Se il PIN è sbagliato, ne crea uno nuovo e lo ridà
        nuovo_pin = create_reset_pin(user["id"])
        flash("Invalid PIN. A new one was generated.", "reset_error")
        flash(nuovo_pin, "reset_pin") 
        return redirect(url_for("casino.lobby"))

# Cancellazione account (SOFT DELETE)
@account.route("/delete", methods=["POST"])
def delete_account():
    # Se non si è loggati, non si può farlo
    if "user_id" not in session:
        abort(403)

    user = get_user_by_id(session["user_id"])
    
    # Un admin non può cancellarsi da solo da qui
    if user["role"] == "admin":
        flash("Admins cannot delete themselves.", "error")
        return redirect(url_for("admin.dashboard"))

    # Log azione e poi cancellazione
    log_admin_action(None, user["id"], "self_delete")
    soft_delete_user(user["id"])
    
    session.clear()
    flash("Account deleted.", "info")
    return redirect(url_for("casino.lobby"))