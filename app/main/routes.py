from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/") # Homepage
def index():
    return render_template("main/index.html")