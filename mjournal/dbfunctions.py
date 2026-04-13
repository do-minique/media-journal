import db

def get_entries():
    sql = """
        SELECT 
            Media.id,
            Media.name,
            Media.description,
            Media.release_year,
            Media.date_added,
            Media.adder_id,
            users.username AS adder_username,
            Mediatypes.name AS mediatype_name
        FROM Media
        JOIN Users ON Media.adder_id = Users.id
        JOIN Mediatypes ON Media.mediatype_id = Mediatypes.id
        ORDER BY Media.date_added DESC
    """
    return db.query(sql) 

def get_entry(entry_id):
    sql = """
        SELECT 
            Media.id,
            Media.name,
            Media.description,
            Media.release_year,
            Media.date_added,
            Media.mediatype_id,
            Media.adder_id,
            Users.username AS adder_username,
            Mediatypes.name AS mediatype_name
        FROM Media
        JOIN Users ON Media.adder_id = Users.id
        JOIN Mediatypes ON Media.mediatype_id = Mediatypes.id
        WHERE Media.id = ?
    """
    result = db.query(sql, (entry_id,))
    return result[0] if result else None
   
def update_entry(entry_id, name, description, release_year, mediatype_id):
    sql = """
        UPDATE Media
        SET name = ?, 
            description = ?, 
            release_year = ?, 
            mediatype_id = ?
        WHERE id = ?
    """
    db.execute(sql, (name, description, release_year, mediatype_id, entry_id))

def delete_entry(entry_id):
    sql = "DELETE FROM Media WHERE id = ?"
    db.execute(sql, [entry_id])

def get_user(user_id):
    sql = "SELECT id, username FROM Users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def search_entries(query):
    sql = """
        SELECT 
            Media.id,
            Media.name,
            Media.description,
            Media.release_year,
            Media.date_added,
            Media.adder_id,
            Users.username AS adder_username,
            Mediatypes.name AS mediatype_name
        FROM Media
        JOIN Users ON Media.adder_id = Users.id
        JOIN Mediatypes ON Media.mediatype_id = Mediatypes.id
        WHERE Media.name LIKE ?
           OR Media.description LIKE ?
           OR Media.release_year LIKE ?
           OR Mediatypes.name LIKE ?
           OR Users.username LIKE ?
        ORDER BY Media.date_added DESC
    """
    like_query = "%" + query + "%"
    return db.query(sql, (like_query, like_query, like_query, like_query, like_query))

def get_reviews_permedia(media_id):
    sql = """
        SELECT
            Reviews.id,
            Reviews.media_id,
            Reviews.user_id,
            Reviews.rating,
            Reviews.comment,
            Reviews.date_added,
            Users.username
        FROM Reviews
        JOIN Users ON Reviews.user_id = Users.id
        WHERE Reviews.media_id = ?
        ORDER BY Reviews.date_added DESC
    """
    return db.query(sql, [media_id])

def get_reviews_peruser(user_id):
    sql = """
        SELECT
            Reviews.id,
            Reviews.media_id,
            Reviews.user_id,
            Reviews.rating,
            Reviews.comment,
            Reviews.date_added,
            Users.username,
            Media.name
        FROM Reviews
        JOIN Users ON Reviews.user_id = Users.id
        JOIN Media ON Reviews.media_id = Media.id
        WHERE Reviews.user_id = ?
        ORDER BY Reviews.date_added DESC
    """
    return db.query(sql, [user_id])

def get_average_rating_peruser(user_id):
    sql = """
        SELECT AVG(rating) as avg_rating
        FROM Reviews
        WHERE user_id = ?
    """
    result = db.query(sql, [user_id])
    return result[0]["avg_rating"] if result else None

def get_review(review_id):
    sql = """
        SELECT
            Reviews.id,
            Reviews.media_id,
            Reviews.user_id,
            Reviews.rating,
            Reviews.comment,
            Reviews.date_added,
            Users.username
        FROM Reviews
        JOIN Users ON Reviews.user_id = Users.id
        WHERE Reviews.id = ?
    """
    result = db.query(sql, (review_id,))
    return result[0] if result else None

def update_review(review_id, comment, rating):
    sql = """
        UPDATE Media
        SET comment = ?, 
            rating = ?, 
        WHERE id = ?
    """
    db.execute(sql, (comment, rating, review_id))

def delete_review(review_id):
    sql = "DELETE FROM Reviews WHERE id = ?"
    db.execute(sql, [review_id])

def get_users():
    sql = """
        SELECT id, username
        FROM Users
        ORDER BY username
    """
    return db.query(sql)