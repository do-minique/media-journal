import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, flash, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
from datetime import datetime
import config
import dbfunctions
import math
import secrets
import markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    user_id = session.get("user_id")
    user = None
    if user_id:
        user = dbfunctions.get_user(user_id)
    return render_template("index.html", user=user)

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

    flash("Account created! You can now log in.")
    return redirect("/typelogin"
    )

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = db.query(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    )

    if len(user) == 0:
        flash("Wrong username or password")
        return redirect("/typelogin")

    user = user[0]

    if not check_password_hash(user["password_hash"], password):
        flash("Wrong username or password")
        return redirect("/typelogin")

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["csrf_token"] = secrets.token_hex(16)
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/listmedia")
@app.route("/listmedia/<int:page>")
def show_media(page=1):
    page_size = 6
    entry_count = dbfunctions.get_entry_count()
    page_count = math.ceil(entry_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/listmedia/1")
    if page > page_count:
        return redirect("/listmedia/" + str(page_count))

    entries = dbfunctions.get_entries(page, page_size)
    return render_template(
        "listmedia.html",
        page=page,
        page_count=page_count,
        entries=entries
    )

@app.route("/add", methods=["GET", "POST"])
def add():
    if session.get("user_id") is None:
        abort(403)

    if request.method == "GET":
        genres = dbfunctions.get_genres()
        return render_template("add.html", genres=genres)

    check_csrf()
    entry_name = request.form["name"]
    entry_type = request.form["type"]
    entry_year = request.form["release_year"]
    entry_desc = request.form["description"]
    genre_ids = request.form.getlist("genre_ids")
    added_by_user = session["user_id"]

    if not entry_name or not entry_type or not entry_year or not entry_desc:
        flash("All fields are required")
        return redirect(url_for("add"))

    try:
        dbfunctions.add_media(
            entry_name,
            entry_desc,
            entry_year,
            entry_type,
            added_by_user,
            genre_ids
        )

        flash("Media entry added successfully")
        return redirect(url_for("index"))

    except sqlite3.IntegrityError as e:
        return f"Database error: {e}"

    except Exception as e:
        return f"Error: {e}"

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
        genres = dbfunctions.get_genres()
        selected_genres = dbfunctions.get_genre_ids_by_media(entry_id)

        return render_template(
            "edit.html",
            entry=entry,
            genres=genres,
            selected_genres=selected_genres
        )

    if request.method == "POST":
        check_csrf()
        name = request.form["name"]
        description = request.form["description"]
        release_year = request.form["release_year"]
        mediatype_id = request.form["mediatype_id"]
        genre_ids = request.form.getlist("genre_ids")

        dbfunctions.update_entry(
            entry_id, name, description, release_year, mediatype_id
        )

        dbfunctions.update_genres(entry_id, genre_ids)

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
        check_csrf()
        if "continue" in request.form:
            dbfunctions.delete_entry(entry["id"])
        return redirect(url_for("show_media"))

@app.route("/search", methods=["GET"])
@app.route("/search/<int:page>", methods=["GET"])
def search(page=1):
    query = request.args.get("query", "").strip()
    genre_id = request.args.get("genre_id", "").strip()
    min_rating_str = request.args.get("min_rating", "").strip()

    min_rating = None
    if min_rating_str:
        min_rating = float(min_rating_str)

    genres = dbfunctions.get_genres()

    page_size = 6
    entry_count = dbfunctions.search_entry_count(
        query,
        genre_id if genre_id else None,
        min_rating if min_rating else None
    )

    page_count = math.ceil(entry_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect(url_for(
            "search",
            page=1,
            query=query,
            genre_id=genre_id,
            min_rating=min_rating
        ))

    if page > page_count:
        return redirect(url_for(
            "search",
            page=page_count,
            query=query,
            genre_id=genre_id,
            min_rating=min_rating
        ))

    if query or genre_id or min_rating:
        entries = dbfunctions.search_entries(
            query,
            genre_id if genre_id else None,
            min_rating if min_rating else None,
            page,
            page_size
        )
    else:
        entries = []

    return render_template(
        "search.html",
        query=query,
        genres=genres,
        selected_genre_id=genre_id,
        min_rating=min_rating,
        entries=entries,
        page=page,
        page_count=page_count
    )

@app.route("/addreview/<int:entry_id>", methods=["GET", "POST"])
def add_review(entry_id):
    entry = dbfunctions.get_entry(entry_id)
    if session.get("user_id") is None:
        abort(403)
    if request.method == "GET":
        return render_template("addreview.html",entry=entry)
    if request.method == "POST":
        check_csrf()
        entry_rating = request.form["rating"]
        entry_comment = request.form["comment"]
        added_by_user = session["user_id"]

        if not entry_rating or not entry_comment:
            return "All fields are required"

        try:
            sql = """
                INSERT INTO Reviews
                (media_id, user_id, rating, comment, date_added)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """
            db.execute(sql, [entry_id, added_by_user, entry_rating, entry_comment])

            flash("Review entry added successfully")
            return redirect(url_for("index"))
        
        except sqlite3.IntegrityError:
            abort(403)

        except Exception as e:
            flash(f"Error: {e}")
            return redirect(url_for("show_media"))
        
@app.route("/listreviews_permedia/<int:entry_id>")
@app.route("/listreviews_permedia/<int:entry_id>/<int:page>")
def show_reviews(entry_id, page=1):
    entry = dbfunctions.get_entry(entry_id)
    if not entry:
        abort(404)

    page_size = 9
    review_count = dbfunctions.get_review_count_permedia(entry_id)
    page_count = math.ceil(review_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect(f"/listreviews_permedia/{entry_id}/1")
    if page > page_count:
        return redirect(f"/listreviews_permedia/{entry_id}/{page_count}")

    reviews = dbfunctions.get_reviews_permedia(entry_id, page, page_size)

    return render_template(
        "listreviews_permedia.html",
        reviews=reviews,
        entry=entry,
        page=page,
        page_count=page_count
    )

@app.route("/editreview/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    review = dbfunctions.get_review(review_id)
    if not review:
        abort(404)
    if session.get("user_id") is None:
        abort(403)
    if review["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("editreview.html", review=review)
 
    if request.method == "POST":
        check_csrf()
        rating = request.form["rating"]
        comment = request.form["comment"]

        dbfunctions.update_review(review_id, comment, rating)
        return redirect(url_for("show_media"))

@app.route("/removereview/<int:review_id>", methods=["GET", "POST"])
def remove_review(review_id):
    review = dbfunctions.get_review(review_id)
    if not review:
        abort(404)
    if session.get("user_id") is None:
        abort(403)
    if review["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("removereview.html", review=review)

    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            dbfunctions.delete_review(review["id"])
        return redirect(url_for("show_media"))

@app.route("/user/<int:user_id>")
@app.route("/user/<int:user_id>/<int:page>")
def show_user(user_id, page=1):
    user = dbfunctions.get_user(user_id)
    if not user:
        abort(404)

    page_size = 6
    review_count = dbfunctions.get_review_count_peruser(user_id)
    page_count = math.ceil(review_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect(f"/user/{user_id}/1")
    if page > page_count:
        return redirect(f"/user/{user_id}/{page_count}")

    reviews = dbfunctions.get_reviews_peruser(user_id, page, page_size)
    avg_rating = dbfunctions.get_average_rating_peruser(user_id)

    return render_template(
        "user.html",
        user=user,
        reviews=reviews,
        avg_rating=avg_rating,
        review_count=review_count,
        page=page,
        page_count=page_count
    )

import math
from flask import render_template, redirect

@app.route("/listusers")
@app.route("/listusers/<int:page>")
def list_users(page=1):
    page_size = 20
    user_count = dbfunctions.get_user_count()
    page_count = math.ceil(user_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/listusers/1")
    if page > page_count:
        return redirect(f"/listusers/{page_count}")

    users = dbfunctions.get_users(page, page_size)

    return render_template(
        "listusers.html",
        users=users,
        page=page,
        page_count=page_count
    )

def check_csrf():
    print("FORM:", request.form)
    if request.form.get("csrf_token") != session.get("csrf_token"):
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)