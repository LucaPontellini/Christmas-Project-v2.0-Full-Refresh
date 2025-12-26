from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.main.routes import main
    from app.casino.routes import casino

    app.register_blueprint(main)
    app.register_blueprint(casino)

    return app