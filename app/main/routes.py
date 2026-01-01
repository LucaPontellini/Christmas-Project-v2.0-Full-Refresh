from flask import Blueprint, render_template

main = Blueprint("main", __name__) # Crea un blueprint per raggruppare le route principali

@main.route("/")  # Route della homepage
def index():
    return render_template("main/index.html")