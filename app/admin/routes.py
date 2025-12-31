from app.database import db
from flask import Blueprint, render_template, session, abort, redirect, url_for, request, flash
from app.admin.repository import (
    get_dashboard_stats, get_all_users, get_access_logs, 
    get_recent_transactions, log_admin_action, soft_delete_user, restore_user, 
    update_user_balance_admin, get_all_bonuses
)
from app.account.repository import get_user_by_id, get_user_by_id_any, hard_delete_user

admin = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required():
    user_id = session.get("user_id")
    if not user_id: abort(404)
    user = get_user_by_id(user_id)
    if not user or user["role"] != "admin": abort(404)
    return user

@admin.route("/dashboard")
def dashboard():
    user = admin_required()
    return render_template(
        "admin/dashboard.html",
        user=user,
        stats=get_dashboard_stats(),
        users=get_all_users(),
        logs=get_access_logs(),
        transactions=get_recent_transactions(),
        available_bonuses=get_all_bonuses()
    )

@admin.route("/users/add-balance/<int:user_id>", methods=["POST"], strict_slashes=False)
def add_balance(user_id):
    admin_required()
    target_user = get_user_by_id(user_id)
    if not target_user or target_user["role"] == "admin":
        flash("Action not allowed.", "error")
        return redirect(url_for("admin.dashboard"))

    action = request.form.get("action")
    try:
        amount = int(request.form.get("amount", 0))
    except ValueError:
        flash("Invalid amount", "error")
        return redirect(url_for("admin.dashboard"))

    if amount <= 0:
        flash("Amount must be greater than zero", "warning")
        return redirect(url_for("admin.dashboard"))

    final_amount = -abs(amount) if action == "sub" else abs(amount)
    
    if (target_user["balance"] + final_amount) < 0:
        flash("Balance cannot be negative", "error")
        return redirect(url_for("admin.dashboard"))

    update_user_balance_admin(user_id, final_amount, "adjustment")
    flash(f"Updated balance for {target_user['username']}", "success")
    return redirect(url_for("admin.dashboard"))

@admin.route("/users/delete/<int:user_id>", methods=["POST"], strict_slashes=False)
def delete_user(user_id):
    admin_required()
    target_user = get_user_by_id(user_id)
    if not target_user or target_user["role"] == "admin": abort(404)
    
    soft_delete_user(user_id)
    log_admin_action(session["user_id"], user_id, "soft_delete")
    flash("User disabled", "success")
    return redirect(url_for("admin.dashboard"))

@admin.route("/users/hard-delete/<int:user_id>", methods=["POST"], strict_slashes=False)
def hard_delete_user_route(user_id):
    admin_required() 
    
    target_user = get_user_by_id_any(user_id) 
    
    if not target_user:
        flash("User not found", "error")
        return redirect(url_for("admin.dashboard"))

    if target_user["role"] == "admin":
        flash("Cannot delete an administrator", "error")
        return redirect(url_for("admin.dashboard"))

    try:
        # 1. Log dell'azione (deve avvenire PRIMA della cancellazione fisica)
        log_admin_action(session["user_id"], user_id, "hard_delete")
        
        # 2. Esecuzione cancellazione fisica di tutti i record collegati
        hard_delete_user(user_id)
        
        flash(f"User {target_user['username']} permanently removed.", "success")
    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
        
    return redirect(url_for("admin.dashboard"))

@admin.route("/user/<int:user_id>/restore", methods=["POST"], strict_slashes=False)
def restore_user_route(user_id):
    admin_required()
    restore_user(user_id)
    log_admin_action(session["user_id"], user_id, "restore")
    flash("User restored successfully", "success")
    return redirect(url_for("admin.dashboard"))