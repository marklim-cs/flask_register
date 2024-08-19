from flask import Flask, request, render_template, redirect

app = Flask(__name__)

SPORTS = ["Aqua Aerobics", "Pilates", "Stretching", "Joga", "Bodypump"]

REGISTRANTS = {}

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")

    REGISTRANTS[name] = sport

    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    return render_template("registrants.html", registrants=REGISTRANTS)

if __name__ == '__main__':
    app.run(debug=True)