
# Media Journal

With Media Journal, users can create a list of movies and series they have watched, as well as books they have read. The user can also write reviews and view statistics.

## Features

- The user can create an account and log in.  
- The user can add, edit, and delete items.  
- The user can assign categories to an item, such as what type it is (movie, book, TV series) and which genre it belongs to.  
- The user can search for their own and others’ items by name or other criteria, such as genre, type, or release year.  
- The user has a profile page where they can view the items they have added and statistics, such as how many movies they have watched or the average rating of their reviews.  
- The user can add a review to an item they have added themselves or one added by another user.


### Current status

In this version, users can create an account and log in, add items when logged in, edit or delete the items they have added, and browse items added by all users. Users can also add/edit/remove reviews. Reviews and statistics can be viewed in user pages.

Supported browsers: Google Chrome, Mozilla Firefox


### Setup instructions

Before you begin, make sure you have the following installed:

- Flask
- SQLite

Testing the application requires first setting up a database on your local machine.

The database schema is stored in the file `schema.sql`. Create the database in a file named `database.db` as follows:

```bash
sqlite3 database.db < schema.sql
```


### Run the application locally

```bash
flask run
```

### Performance

The database was populated with 1000 users, 100 000 media entries and 100 000 reviews for performance testing purposes using the seed.py script. 

Without indices, browsing media entries with large amounts of data took several seconds. For example, navigating from one page to another in the entry listing:
```bash
elapsed time: 1.29 s
127.0.0.1 - - [01/May/2026 12:53:45] "GET /listmedia HTTP/1.1" 200 -
elapsed time: 2.41 s
127.0.0.1 - - [01/May/2026 12:53:49] "GET /listmedia/2 HTTP/1.1" 200 -
elapsed time: 1.02 s
127.0.0.1 - - [01/May/2026 12:53:55] "GET /listreviews_permedia/48300 HTTP/1.1" 200 -
```

The search function froze and did not complete within ten minutes, at which point I terminated the search.


Indices added:
```bash
CREATE INDEX idx_media_date_added ON Media(date_added DESC);
CREATE INDEX idx_reviews_media_id_rating ON Reviews(media_id, rating);
CREATE INDEX idx_reviews_media_date ON Reviews(media_id, date_added DESC);
CREATE INDEX idx_reviews_user_date ON Reviews(user_id, date_added DESC);
CREATE INDEX idx_genrelist_genre_media ON Genrelist(genre_id, media_id);
```


After this, the listings open instantly:
```bash
elapsed time: 0.17 s
127.0.0.1 - - [01/May/2026 13:07:54] "GET /listmedia HTTP/1.1" 200 -
elapsed time: 0.17 s
127.0.0.1 - - [01/May/2026 13:08:45] "GET /listmedia/100 HTTP/1.1" 200 -
elapsed time: 0.02 s
127.0.0.1 - - [01/May/2026 13:08:57] "GET /listreviews_permedia/48305 HTTP/1.1" 200 -

```
Search function:
```bash
elapsed time: 0.24 s
127.0.0.1 - - [01/May/2026 13:10:48] "GET /search?query=&genre_id=4&min_rating=3 HTTP/1.1" 200 -
```
The test showed that adding indices significantly improved performance.




