import sqlite3
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, g

app = Flask(__name__)

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")

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

@app.route("/deregister", methods=["POST"])
def deregister():
    id = request.form.get("id")
    db = get_db()
    if id:
        db.execute("DELETE FROM list_registrants WHERE id = ?", (id,))
        db.commit()
    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    db = get_db()
    list_registrants = db.execute("SELECT * FROM list_registrants")
    return render_template("registrants.html", list_registrants=list_registrants)

if __name__ == '__main__':
    app.run(debug=True)