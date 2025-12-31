from flask import Blueprint, render_template

# Crea un blueprint per raggruppare le route principali
main = Blueprint("main", __name__)

@main.route("/")  # Route della homepage
def index():
    return render_template("main/index.html")