CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE Mediatypes (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE Media (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    release_year INTEGER,
    mediatype_id INTEGER REFERENCES Mediatypes,
    adder_id INTEGER REFERENCES Users,
    date_added TIMESTAMP
);

CREATE TABLE Genres (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Genrelist (
    media_id INTEGER REFERENCES Media,
    genre_id INTEGER REFERENCES Genres,
    PRIMARY KEY (media_id, genre_id)
);

CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    media_id INTEGER REFERENCES Media,
    user_id INTEGER REFERENCES Users,
    rating INTEGER,
    comment TEXT,
    date_added TIMESTAMP
);

INSERT INTO Genres (name) VALUES
  ('Fantasy'),
  ('Scifi'),
  ('Horror'),
  ('Comedy'),
  ('Romance'),
  ('Drama'),
  ('Action');