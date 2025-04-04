from flask import (
    Blueprint, request, url_for, make_response, request, jsonify
)

from flaskr.db import get_db

import os
import pdb
from werkzeug.utils import secure_filename
from flaskr.models.movie import Movie
from flaskr.models.genre import Genre
from flaskr.db import insert_movie
from sqlite3 import IntegrityError
from datetime import datetime, timedelta

UPLOAD_FOLDER = 'flaskr/static/images'

bp = Blueprint('mymovies_blueprint', __name__, url_prefix='/mymovies')


def execute_sql_and_fetch(conn, sql, params=()):
    """Helper function to execute SQL commands."""
    conn = get_db()
    cursor = conn.cursor()
    data = cursor.execute(sql, params).fetchall()
    conn.close()
    return data

def execute_sql(conn, sql, params=()):
    """Helper function to execute SQL commands."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    conn.close()
    return None

@bp.route('/', methods=['POST'])
def add_movie():
    """Endpoint to add a movie."""
    data = request.form
    genre = data.get('genre')
    title = data.get('title')
    rating = data.get('rating')
    comment = data.get('comment')
    director = data.get('director')
    year = data.get('year')
    view_date = data.get('view_date')
    # Check if an image is included in the request
    image_path = None
    if 'image' in request.files:
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)

    movie_entry = Movie(
        genre=Genre(genre),
        title=title,
        rating=rating,
        comment=comment,
        director=director,
        year=year,
        image=image_path,
        view_date=view_date
    )
    conn = get_db()
    try:
        insert_movie(movie_entry, conn)
    except IntegrityError as e:
        conn.close()
        print(f"Integrity Error: {e}")  # Likely a PRIMARY KEY constraint violation
        return jsonify({"error": "Movie with this title, view_date, and year already exists!"}), 409  # HTTP status code for conflict
    except Exception as e:
        conn.close()
        print(f"Unexpected Error: {e}")  # General error handling
        return jsonify({"error": "Unexpected error"}), 500  # HTTP status code for internal server error
    conn.commit()
    conn.close()

    return jsonify({"message": "Movie added successfully!", "movie": movie_entry.json()}), 201


@bp.route('/', methods=['GET'])
def get_all_movies():
    """Endpoint to retrieve all movies."""
    conn = get_db()
    cursor = conn.cursor()
    movies = cursor.execute(
        'SELECT director, movie_id FROM movies ORDER BY director DESC'
    ).fetchall()
    conn.close()
    # Convert rows to dictionaries directly
    movies_list = [dict(movie) for movie in movies]
    response = make_response(jsonify(movies_list), 200)
    # Set Cache-Control and Expires headers to cache the response for 1 hour on the CLIENT SIDE!
    response.headers["Cache-Control"] = "public, max-age=3600"  # Cache for 1 hour
    response.headers["Expires"] = (datetime.now() + timedelta(hours=1)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    return response


@bp.route('/genres/<genre>', methods=['GET'])
def get_movies_by_genre(genre):
    """Endpoint to retrieve movies by genre."""
    conn = get_db()
    cursor = conn.cursor()
    movies = cursor.execute(
        'SELECT * FROM movies WHERE genre = ? ORDER BY director DESC', (genre,)
    ).fetchall()
    conn.close()
    # Convert rows to dictionaries directly
    movies_list = [dict(movie) for movie in movies]
    if not movies_list:
        return jsonify({"error": "No movies found for this genre"}), 404

    return jsonify(movies_list), 200


@bp.route('/genres', methods=['GET'])
def get_all_genres():
    """Endpoint to retrieve all genres."""
    return jsonify([genre.value for genre in Genre]), 200


@bp.route('/directors', methods=['GET'])
def get_all_directors():
    """Endpoint to retrieve all directors."""
    conn = get_db()
    cursor = conn.cursor()
    directors = cursor.execute(
        "SELECT DISTINCT director FROM movies"
    ).fetchall()
    conn.close()
    directors_list = [str(director[0]) for director in directors]

    return jsonify(directors_list), 200


@bp.route("/directors/<string:director>", methods=["GET"])
def get_movies_by_director(director):
    conn = get_db()
    cursor = conn.cursor()
    movies = cursor.execute(
        "SELECT movie_id FROM movies WHERE LOWER(REPLACE(director, ' ', '')) = LOWER(REPLACE(?, ' ', '')) ORDER BY movie_id DESC", (director, )
    ).fetchall()
    conn.close()
    # Convert rows to dictionaries directly
    if not movies:
        return jsonify({"error": f"No movies found for this director: {director}"}), 404

    movies_list = []
    for movie in movies:
        movie = dict(movie)
        movie["href"] = url_for("get_movie_by_id", id=movie["movie_id"], _external=True)
        movies_list.append(movie)

    return jsonify(movies_list), 200


@bp.route("/id/<string:movie_id>", methods=["GET", "PUT"])
def get_movie_by_id(movie_id):
    if request.method == 'GET':
        conn = get_db()
        cursor = conn.cursor()
        movies = cursor.execute(
            "SELECT * FROM movies WHERE movie_id = ?", (movie_id, )
        ).fetchall()
        conn.close()
        # Convert rows to dictionaries directly
        movies_list = [dict(movie) for movie in movies]
        if not movies_list:
            message = f"No movies found for this movie id: {movie_id}"
            status_code = 404
        else:
            message = jsonify(movies_list)
            status_code = 200

    elif request.method == 'PUT':
        # pdb.set_trace()
        data = request.form
        genre = data.get('genre')
        rating = data.get('rating')
        comment = data.get('comment')
        director = data.get('director')

        conn = get_db()
        cursor = conn.cursor()
        # Update the movie with the given movie_id
        cursor.execute(
            "UPDATE movies SET genre = ?, director = ?, rating = ?, comment = ? WHERE movie_id = ?",
            (genre, director, rating, comment, movie_id)
        )
        conn.commit()
        conn.close()
        message = jsonify({"message": f"Movie with movie_id {movie_id} updated successfully!"})
        status_code = 200 

    return message, status_code


@bp.route("/title/<string:title>", methods=["GET"])
def get_movie_by_title(title):
    conn = get_db()
    cursor = conn.cursor()
    movies = cursor.execute(
        "SELECT * FROM movies WHERE LOWER(REPLACE(title, ' ', '')) = LOWER(REPLACE(?, ' ', ''))", (title, )
    ).fetchall()
    conn.close()
    # Convert rows to dictionaries directly
    movies_list = [dict(movie) for movie in movies]
    if not movies_list:
        return jsonify({"error": f"No movies found for this movie title: {title}"}), 404

    return jsonify(movies_list), 200


@bp.route("/delete/id/<string:movie_id>", methods=["DELETE"])
def delete_movie_id(movie_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE movie_id = ?", (movie_id, ))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Movie with movie_id {movie_id} deleted successfully!"}), 204


@bp.route("/delete/title/<string:title>", methods=["DELETE"])
def delete_movie_title(title):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE LOWER(REPLACE(title, ' ', '')) = LOWER(REPLACE(?, ' ', ''))", (title, ))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Movie with title {title} deleted successfully!"}), 204


