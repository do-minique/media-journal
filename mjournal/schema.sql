CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE CHECK (trim(username) <> ''),
    password_hash TEXT NOT NULL
);

CREATE TABLE Mediatypes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Media (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    release_year INTEGER CHECK (release_year >= 0),
    mediatype_id INTEGER NOT NULL REFERENCES Mediatypes(id),
    adder_id INTEGER NOT NULL REFERENCES Users(id),
    date_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Genres (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Genrelist (
    media_id INTEGER NOT NULL REFERENCES Media(id),
    genre_id INTEGER NOT NULL REFERENCES Genres(id),
    PRIMARY KEY (media_id, genre_id)
);

CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    media_id INTEGER NOT NULL REFERENCES Media(id),
    user_id INTEGER NOT NULL REFERENCES Users(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 10),
    comment TEXT,
    date_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Mediatypes (id, name) VALUES
(1, 'Book'),
(2, 'Movie'),
(3, 'TV show');

INSERT INTO Genres (name) VALUES
  ('Fantasy'),
  ('Scifi'),
  ('Horror'),
  ('Comedy'),
  ('Romance'),
  ('Drama'),
  ('Action');
