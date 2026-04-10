import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, flash, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
from datetime import datetime
import config
import dbfunctions

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    user_id = session.get("user_id")
    username = None
    if user_id:
        username = dbfunctions.get_username(user_id)
    return render_template("index.html", username=username)

@app.route("/typelogin")
def typelogin():
    return render_template("typelogin.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return render_template(
            "register.html",
            error="ERROR: passwords do not match",
            username=username
        )

    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template(
            "register.html",
            error="ERROR: username is already taken",
            username=username
        )

    return render_template(
        "register.html",
        success="Account created! You can now log in."
    )

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = db.query(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    )

    if len(user) == 0:
        return render_template("index.html", error="ERROR: wrong username or password")

    user = user[0]

    if not check_password_hash(user["password_hash"], password):
        return render_template("index.html", error="ERROR: wrong username or password")

    session["user_id"] = user["id"]
    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

@app.route("/listmedia")
def show_media():
    entries = dbfunctions.get_entries()
    if not entries:
        abort(404)
    return render_template("listmedia.html", entries=entries)

@app.route("/add")
def add():
    if session.get("user_id") is None:
        abort(403)
    return render_template("add.html")

@app.route("/added", methods=["POST"])
def added():
    entry_name = request.form["name"]
    entry_type = request.form["type"]
    entry_year = request.form["release_year"]
    entry_desc = request.form["description"]
    added_by_user = session["user_id"]

    if not entry_name or not entry_type or not entry_year or not entry_desc:
        return "All fields are required"

    try:
        sql = """
            INSERT INTO Media
            (name, description, release_year, mediatype_id, adder_id, date_added)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        db.execute(sql, [entry_name, entry_desc, entry_year, entry_type, added_by_user])

        flash("Media entry added successfully")
        return redirect(url_for("index"))
        
    except sqlite3.IntegrityError:
        abort(403)

    except Exception as e:
        flash(f"Error: {e}")
        return redirect(url_for("add"))

@app.route("/edit/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = dbfunctions.get_entry(entry_id)
    if not entry:
        abort(404)
    if session.get("user_id") is None:
        abort(403)
    if entry["adder_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", entry=entry)
 
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        release_year = request.form["release_year"]
        mediatype_id = request.form["mediatype_id"]

        dbfunctions.update_entry(entry_id, name, description, release_year, mediatype_id)
        return redirect(url_for("show_media"))

@app.route("/remove/<int:entry_id>", methods=["GET", "POST"])
def remove_entry(entry_id):
    entry = dbfunctions.get_entry(entry_id)
    if not entry:
        abort(404)
    if session.get("user_id") is None:
        abort(403)
    if entry["adder_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", entry=entry)

    if request.method == "POST":
        if "continue" in request.form:
            dbfunctions.delete_entry(entry["id"])
        return redirect(url_for("show_media"))

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()

    if query:
        entries = dbfunctions.search_entries(query)
    else:
        entries = []

    return render_template("search.html", query=query, entries=entries)
        
