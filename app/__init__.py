import os
from flask import Flask, session, g

from app.account.repository import get_user_by_id
from app.utils.color import get_user_initial, get_user_color


def create_app():
    app = Flask(__name__)

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.secret_key = os.environ.get("SECRET_KEY", "dev-key")

    # === BLUEPRINTS ===
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

    # === TEMPLATE CONTEXT ===
    @app.context_processor
    def inject_user():
        user = None
        user_initial = None
        user_color = None

        if "user_id" in session:
            user = get_user_by_id(session["user_id"])
            if user:
                user_initial = get_user_initial(user["username"])
                user_color = get_user_color(user["username"])

        return dict(
            user=user,
            user_initial=user_initial,
            user_color=user_color
        )

    # === GLOBAL USER (PYTHON) ===
    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")
        g.user = get_user_by_id(user_id) if user_id else None

    return app