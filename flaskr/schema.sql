DROP TABLE IF EXISTS movies;

CREATE TABLE movies (
    title TEXT NOT NULL,
    director TEXT NOT NULL,
    genre TEXT,
    year INTEGER NOT NULL,
    rating REAL,
    comment TEXT,
    view_date TEXT NOT NULL,
    image TEXT,
    movie_id TEXT GENERATED ALWAYS AS (
        SUBSTR(view_date, 3, 2) || SUBSTR(view_date, 6, 2) || SUBSTR(view_date, 9, 2) ||
        UPPER(REPLACE(title, ' ', '')) ||
        year
    ) STORED UNIQUE,
    PRIMARY KEY (title, view_date, year)
);