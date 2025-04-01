import sqlite3
import click
from flask import current_app, g
from flaskr.init_movies import MOVIES
from flaskr.models.movie import Movie


def get_db() -> sqlite3.Connection:
    '''
    g is a special object that is unique for each request.
    It is used to store data that might be accessed by multiple functions during the request.
    The connection is stored and reused instead of creating a new connection if get_db is called a second time in the same request.

    current_app is another special object that points to the Flask application handling the request.
    Since you used an application factory, there is no application object when writing the rest of your code.
    get_db will be called when the application has been created and is handling a request, so current_app can be used.
    '''
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def insert_movie(movie: Movie, conn: sqlite3.Connection):
    """Inserts a Pydantic Movie object into the SQLite database."""
    cursor = conn.cursor()
    cursor.execute(
    '''
    INSERT INTO movies (title, genre, director, year, rating, comment, view_date, image)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''',
    (
        movie.title, movie.genre.value, movie.director, movie.year, 
        movie.rating, movie.comment, movie.view_date, movie.image)
    )
    print("Movie inserted successfully!")  # HTTP status code for created


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    for movie in MOVIES:
        insert_movie(movie, db)
    db.commit()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)