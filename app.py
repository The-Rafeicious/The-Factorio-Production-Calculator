from math import ceil

from flask import Flask, render_template, request
from config import BELT_SPEEDS
from smelting_form_processing import smelting_form_base

app = Flask(__name__)

@app.route("/")
def MainMenu():
    return render_template("main_HTML.html")

@app.route("/smelting-form", methods=["GET", "POST"])
def smelting_form():
    if request.method == "POST":
        raw_data = request.form

        final_data = smelting_form_base(raw_data)

        return render_template("results_HTML.html", results=final_data)

    return render_template("smelting_form_HTML.html")

if __name__ == "__main__":
    app.run(debug=True)