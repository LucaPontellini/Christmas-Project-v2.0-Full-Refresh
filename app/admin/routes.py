from app.database import db
from flask import Blueprint, render_template, session, abort, redirect, url_for, request, flash
from app.admin.repository import get_dashboard_stats, get_all_users, get_recent_transactions, log_admin_action, soft_delete_user, restore_user, update_user_balance_admin, get_all_bonuses, get_system_activity
from app.account.repository import get_user_by_id, get_user_by_id_any, hard_delete_user

# Blueprint dell'area admin
admin = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required():
    # Controllo presenza sessione utente
    user_id = session.get("user_id")
    if not user_id:
        abort(404)

    # Recupero utente e verifica ruolo admin
    user = get_user_by_id(user_id)
    if not user or user["role"] != "admin":
        abort(404)

    return user

@admin.route("/dashboard") # Dashboard route
def dashboard():
    # Accesso consentito solo agli admin
    user = admin_required()

    # Log di sistema recenti
    system_logs = get_system_activity(limit=20)

    # Rendering della dashboard con tutti i dati aggregati
    return render_template("admin/dashboard.html", user=user, stats=get_dashboard_stats(), users=get_all_users(), logs=system_logs, transactions=get_recent_transactions(), available_bonuses=get_all_bonuses())

@admin.route("/users/add-balance/<int:user_id>", methods=["POST"], strict_slashes=False) # Add / Subtract balance route
def add_balance(user_id):
    # Verifica permessi admin
    admin_required()

    # Recupero utente target
    target_user = get_user_by_id(user_id)

    # Utente inesistente
    if not target_user:
        flash("Action not allowed: user not found.", "error")
        return redirect(url_for("admin.dashboard"))

    # Blocco operazioni su admin
    if target_user["role"] == "admin":
        flash("Action not allowed: cannot modify admin balance.", "error")
        return redirect(url_for("admin.dashboard"))

    # Tipo operazione (add / sub)
    action = request.form.get("action")

    # Parsing importo
    try:
        amount = int(request.form.get("amount", 0))
    except ValueError:
        flash("Invalid amount format. Please enter a number.", "error")
        return redirect(url_for("admin.dashboard"))

    # Importo non valido
    if amount <= 0:
        flash("Amount must be greater than zero.", "warning")
        return redirect(url_for("admin.dashboard"))

    # + / - Logica operazione
    is_subtraction = action == "sub"
    normalized_amount = abs(amount)

    if is_subtraction:
        final_amount = -normalized_amount
    else: final_amount = normalized_amount

    # Controllo saldo negativo
    current_balance = target_user["balance"]
    new_balance = current_balance + final_amount

    if new_balance < 0:
        flash("Balance cannot be negative.", "error")
        return redirect(url_for("admin.dashboard"))

    # Aggiornamento saldo
    update_user_balance_admin(user_id, final_amount, "adjustment")

    # Log azione admin
    log_admin_action(session["user_id"], user_id, f"balance_adjustment ({final_amount}€)")

    # Conferma
    flash(f"Updated balance for {target_user['username']} ({final_amount:+}€)", "success")

    return redirect(url_for("admin.dashboard"))

@admin.route("/users/delete/<int:user_id>", methods=["POST"], strict_slashes=False) # Soft delete user route
def delete_user(user_id):
    # Verifica permessi admin
    admin_required()

    # Recupero utente e blocco eliminazione admin
    target_user = get_user_by_id(user_id)
    if not target_user or target_user["role"] == "admin":
        abort(404)
    
    # Soft delete + log
    soft_delete_user(user_id)
    log_admin_action(session["user_id"], user_id, "soft_delete")

    flash("User disabled", "success")
    return redirect(url_for("admin.dashboard"))

@admin.route("/users/hard-delete/<int:user_id>", methods=["POST"], strict_slashes=False) # Hard delete user route
def hard_delete_user_route(user_id):
    # Verifica permessi admin
    admin_required()
    
    # Recupero utente anche se disabilitato
    target_user = get_user_by_id_any(user_id)
    
    # Blocco operazioni su utenti inesistenti o admin
    if not target_user:
        flash("User not found", "error")
        return redirect(url_for("admin.dashboard"))

    if target_user["role"] == "admin":
        flash("Cannot delete an administrator", "error")
        return redirect(url_for("admin.dashboard"))

    # Eliminazione definitiva con gestione errori
    try:
        log_admin_action(session["user_id"], user_id, "hard_delete")
        hard_delete_user(user_id)
        flash(f"User {target_user['username']} permanently removed.", "success")
    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
        
    return redirect(url_for("admin.dashboard"))

@admin.route("/user/<int:user_id>/restore", methods=["POST"], strict_slashes=False) # Restore user route
def restore_user_route(user_id):
    # Verifica permessi admin
    admin_required()

    # Ripristino utente + log
    restore_user(user_id)
    log_admin_action(session["user_id"], user_id, "restore")

    flash("User restored successfully", "success")
    return redirect(url_for("admin.dashboard"))