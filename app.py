from math import ceil

from flask import Flask, render_template, request, session, redirect, url_for
from config import BELT_SPEEDS
from smelting_form_processing import smelting_form_base

app = Flask(__name__)
app.secret_key = "super_secret_factorio_key"

@app.route("/")
def MainMenu():
    return render_template("main_HTML.html")

@app.route("/smelting-form", methods=["GET", "POST"])
def smelting_form():
    if request.method == "POST":
        raw_data = request.form

        session['results'] = smelting_form_base(raw_data)

        return redirect(url_for('smelting_results'))

    return render_template("smelting_form_HTML.html")

@app.route("/smelting-results", methods=["GET", "POST"])
def smelting_results():
    final_data = session.get("results")

    if not final_data:
        return redirect(url_for('MainMenu'))

    return render_template("results_HTML.html", results=final_data)



if __name__ == "__main__":
    app.run(debug=True)