import random
import sqlite3
from werkzeug.security import generate_password_hash

db = sqlite3.connect("database.db")
db.execute("PRAGMA foreign_keys = ON")

db.execute("DELETE FROM Reviews")
db.execute("DELETE FROM Genrelist")
db.execute("DELETE FROM Media")
db.execute("DELETE FROM Users")

user_count = 1000
media_count = 100000
review_count = 1000000

password_hash = generate_password_hash("password")

for i in range(1, user_count + 1):
    db.execute(
        "INSERT INTO Users (username, password_hash) VALUES (?, ?)",
        [f"user{i}", password_hash]
    )


for i in range(1, media_count + 1):
    mediatype_id = random.randint(1, 3)
    adder_id = random.randint(1, user_count)
    release_year = random.randint(0, 2026)

    db.execute("""
        INSERT INTO Media
        (name, description, release_year, mediatype_id, adder_id, date_added)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, [
        f"media{i}",
        f"description for media {i}",
        release_year,
        mediatype_id,
        adder_id
    ])

    media_id = i

    genre_ids = random.sample(range(1, 6), random.randint(1, 3))

    for genre_id in genre_ids:
        db.execute(
            "INSERT INTO Genrelist (media_id, genre_id) VALUES (?, ?)",
            [media_id, genre_id]
        )

for i in range(1, review_count + 1):
    media_id = random.randint(1, media_count)
    user_id = random.randint(1, user_count)
    rating = random.randint(1, 10)

    db.execute("""
        INSERT INTO Reviews
        (media_id, user_id, rating, comment, date_added)
        VALUES (?, ?, ?, ?, datetime('now'))
    """, [
        media_id,
        user_id,
        rating,
        f"review comment {i}"
    ])

db.commit()
db.close()
