import sqlite3
from flask import Flask, request, render_template, redirect, g

app = Flask(__name__)

DATABASE = '/Users/marinaclimovici/dev/flask_training/flask_training/fitness.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


SPORTS = ["Aqua Aerobics", "Pilates", "Stretching", "Yoga", "Bodypump"]

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")

    db = get_db()
    db.execute("INSERT INTO list_registrants (name, sport) VALUES(?, ?)", (name, sport))
    db.commit()

    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    db = get_db()
    list_registrants = db.execute("SELECT * FROM list_registrants")
    return render_template("registrants.html", list_registrants=list_registrants)

if __name__ == '__main__':
    app.run(debug=True)