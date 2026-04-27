
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



