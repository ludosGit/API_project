import sqlite3
from models.genre import Genre
from models.movie import Movie


# Database file path
DB_FILE = "instance/movies.db"

MOVIES = [
    Movie(
        genre=Genre.WAR,
        title="Paths of Glory",
        rating=5,
        comment="Again great movie!",
        director="Stanley Kubrick",
        year=1957,
        view_date="2020-01-15",
        image="/static/images/paths_of_glory.jpg"
    ),
    Movie(
        genre=Genre.WAR,
        title="Paths of Glory",
        rating=5,
        comment="Great movie!",
        director="Stanley Kubrick",
        year=1957,
        view_date="2019-01-01",
        # image="/static/images/inception.jpg"
    ),
    Movie(
        genre=Genre.DRAMA,
        title="Perfect Days",
        director="Wim Wenders",
        year=2023,
        rating=5,
        comment="Great movie! Japanese public toilettes are awesome.",
        view_date="2024-10-15",
    ),
    Movie(
        genre=Genre.THRILLER,
        title="Conclave",
        director="Edward Berger",
        year=2024,
        rating=3,
        comment="What a pope! Watched with Brando and his mum.",
        view_date="2024-12-27",
    )
]

def insert_movie(movie: Movie, conn: sqlite3.Connection):
    """Inserts a Pydantic Movie object into the SQLite database."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO movies (title, genre, director, year, rating, comment, view_date, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (movie.title, movie.genre.value, movie.director, movie.year, 
        movie.rating, movie.comment, movie.view_date, movie.image)
    )
    print("Movie inserted successfully!")  # HTTP status code for created


def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create movies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            title TEXT NOT NULL,
            director TEXT NOT NULL,
            genre TEXT,
            year INTEGER NOT NULL,
            rating REAL,
            comment TEXT,
            view_date TEXT NOT NULL,
            image TEXT,
            PRIMARY KEY (title, view_date, year)
        )
    ''')

    # cursor.executemany('''
    #     INSERT INTO movies (title, director, genre, year, rating, comment, view_date)
    #     VALUES (?, ?, ?, ?, ?, ?, ?)
    # ''', MOVIES)
    for movie in MOVIES:
        insert_movie(movie, conn)

    conn.commit()
    conn.close()
    print("Database created and populated successfully.")

def get_db():
    conn = sqlite3.connect(DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    # tells the connection to return rows that behave like dicts. This allows accessing the columns by name.
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    create_database()
