from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def MainMenu():
    return render_template("main_HTML.html")

@app.route("/smelting-form", methods=["GET", "POST"])
def smelting_form():
    if request.method == "POST":
        ore = request.form["ore"]
        belt = request.form["belt"]
        belt_amount = request.form["belt_amount"]
        furnace = request.form["furnace"]
        return f'received ore: {ore}'
    return render_template("smelting_form_HTML.html")

if __name__ == "__main__":
    app.run(debug=True)