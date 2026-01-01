import os
from flask import Flask, session, g

from app.account.repository import get_user_by_id
from app.utils.color import get_user_initial, get_user_color


def create_app():
    app = Flask(__name__)

    # Configurazione di base della sessione
    app.config["SESSION_PERMANENT"] = False          # La sessione scade alla chiusura del browser
    app.config["SESSION_COOKIE_HTTPONLY"] = True     # Impedisce accesso ai cookie via JavaScript
    app.secret_key = os.environ.get("SECRET_KEY", "dev-key")  # Chiave per firmare le sessioni

    # Registrazione dei blueprint dell'applicazione
    from app.main.routes import main
    from app.casino.routes import casino
    from app.account.routes import account
    from app.admin.routes import admin
    from app.bonus.routes import bonus_bp

    app.register_blueprint(main)
    app.register_blueprint(casino)
    app.register_blueprint(account)
    app.register_blueprint(admin)
    app.register_blueprint(bonus_bp)

    # Variabili disponibili automaticamente nei template Jinja
    @app.context_processor
    def inject_user():
        user = None
        user_initial = None
        user_color = None

        # Se l'utente è loggato, recupera i suoi dati
        if "user_id" in session:
            user = get_user_by_id(session["user_id"])
            if user:
                user_initial = get_user_initial(user["username"])
                user_color = get_user_color(user["username"])

        # Queste variabili saranno disponibili in tutti i template
        return dict(user=user, user_initial=user_initial, user_color=user_color)

    # Carica l'utente loggato prima di ogni richiesta
    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")

        if user_id is None:
            # Nessun utente loggato
            g.user = None
        else:
            # Recupera l'utente dal database
            user = get_user_by_id(user_id)

            if user:
                # Utente valido trovato
                g.user = user
            else:
                # Sessione orfana: l'ID non corrisponde più a un utente reale
                session.clear()   # Invalida la sessione
                g.user = None     # Evita stati incoerenti

    return app