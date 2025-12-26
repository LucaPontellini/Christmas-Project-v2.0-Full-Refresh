from flask import Blueprint, render_template

casino = Blueprint("casino", __name__, url_prefix="/casino")

@casino.route("/")
def lobby():
    return render_template("casino/lobby.html")