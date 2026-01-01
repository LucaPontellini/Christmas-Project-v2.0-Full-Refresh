from flask import Blueprint, render_template, redirect, url_for, session, flash

from app.account.repository import get_user_by_id
from app.bonus.repository import get_user_bonuses, get_registration_bonus
from app.utils.color import get_user_color, get_user_initial

casino = Blueprint("casino", __name__, url_prefix="/casino") # Blueprint per tutte le rotte dell'area Casino

# Lobby (pagina principale)
@casino.route("/")
def lobby():
    # Default per utenti non loggati
    user = None
    user_color = None
    user_initial = None
    registration_bonuses = {}
    
    # Prepara una lista per ricordare quali bonus l'utente ha già preso
    claimed_types = set()

    if "user_id" in session:
        user = get_user_by_id(session["user_id"])

        # Se l'utente non esiste più nel database (ma la sessione è attiva), resetta
        if not user:
            session.clear()
            return redirect(url_for("casino.lobby"))
        
        # Se l'utente esiste, recupera i suoi dati estetici
        user_color = get_user_color(user["username"])
        user_initial = get_user_initial(user["username"])

        # Gestione bonus: solo se l'utente NON è un admin
        if user["role"] != "admin":
            user_bonuses = get_user_bonuses(user["id"])
            
            # controlla i bonus uno per uno
            for b in user_bonuses:
                if b["is_activated"]:
                    # Aggiunge alla nostra lista il metodo ('spid' o 'classic')
                    claimed_types.add(b["method"])

    # Definisce i tipi che si vogliamo gestire
    bonus_types = ["spid", "classic"]

    for b_type in bonus_types:
        # Cerca se questo bonus è attivo nel database
        bonus_data = get_registration_bonus(b_type)
        
        # Creia lo schema base per questo specifico bonus
        info_bonus = {
            "available": False,
            "amount": 0,
            "claimed": False
        }

        # Se il bonus esiste nel database, aggiorna i dati nello schema
        if bonus_data:
            info_bonus["available"] = True
            info_bonus["amount"] = bonus_data["amount"]
            
            # Verifica se l'utente loggato lo ha già riscattato
            if user:
                if b_type in claimed_types:
                    info_bonus["claimed"] = True
                else: info_bonus["claimed"] = False
            else: info_bonus["claimed"] = False # Se non c'è un utente loggato, non può essere "claimed"
        
        # Inserisce lo schema completato nel dizionario principale
        registration_bonuses[b_type] = info_bonus

    return render_template("casino/lobby.html", user=user, user_color=user_color, user_initial=user_initial, registration_bonuses=registration_bonuses)

# Play (placeholder)
@casino.route("/play")
def play(): # Accesso consentito solo agli utenti loggati
    if "user_id" not in session:
        return redirect(url_for("casino.lobby", open="login"))

    # Funzionalità non ancora implementata
    flash("La sezione giochi non è ancora disponibile.", "info")
    return redirect(url_for("casino.lobby"))

# Gioco specifico (placeholder)
@casino.route("/play/<game>")
def play_game(game):
    if "user_id" not in session:
        return redirect(url_for("casino.lobby", open="login"))

    flash("Questo gioco non è ancora disponibile.", "info")
    return redirect(url_for("casino.lobby"))

# Cashier (disabilitato)
@casino.route("/cashier")
def cashier():
    if "user_id" not in session:
        return redirect(url_for("casino.lobby", open="login"))

    flash("La sezione cassiere non è ancora disponibile.", "info")
    return redirect(url_for("casino.lobby"))