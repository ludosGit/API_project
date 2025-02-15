import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from models.movie import Movie
from models.genre import Genre
from sqlite_movies_db import get_db, insert_movie
from sqlite3 import IntegrityError

UPLOAD_FOLDER = 'static/images'

app = Flask(
    __name__,
    static_url_path='/static'
)

@app.route('/mymovies', methods=['POST'])
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

# @app.route("/")
# def hello():
#     return "Hello, these are my favourite movies!"

# Route to render HTML page
@app.route("/", methods=["GET"])
def index():
    return render_template("movie_frontend.html")

@app.route('/mymovies', methods=['GET'])
def get_all_movies():
    """Endpoint to retrieve all movies."""
    conn = get_db()
    cursor = conn.cursor()
    movies = cursor.execute(
        'SELECT * FROM movies ORDER BY director DESC'
    ).fetchall()
    conn.close()
    # Convert rows to dictionaries directly
    movies_list = [dict(movie) for movie in movies]
    return jsonify(movies_list), 200

@app.route('/mymovies/<genre>', methods=['GET'])
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

@app.route('/mymovies/genres', methods=['GET'])
def get_all_genres():
    """Endpoint to retrieve all genres."""
    return jsonify([genre.value for genre in Genre]), 200

@app.route("/mymovies/directors/<string:director>", methods=["GET"])
def get_movies_by_director(director):
    conn = get_db()
    cursor = conn.cursor()
    movies = cursor.execute(
        "SELECT * FROM movies WHERE LOWER(REPLACE(director, ' ', '')) = LOWER(REPLACE(?, ' ', '')) ORDER BY director DESC", (director, )
    ).fetchall()
    conn.close()
    # Convert rows to dictionaries directly
    movies_list = [dict(movie) for movie in movies]
    if not movies_list:
        return jsonify({"error": f"No movies found for this director: {director}"}), 404

    return jsonify(movies_list), 200

@app.route("/mymovies/directors/<string:director>/<string:title>", methods=["GET"])
def get_movie_by_title(director, title):
    conn = get_db()
    cursor = conn.cursor()
    movies = cursor.execute(
        "SELECT * FROM movies WHERE LOWER(REPLACE(director, ' ', '')) = LOWER(REPLACE(?, ' ', ''))"
        " AND LOWER(REPLACE(title, ' ', '')) = LOWER(REPLACE(?, ' ', '')) ORDER BY director DESC", (director, title)
    ).fetchall()
    conn.close()
    # Convert rows to dictionaries directly
    movies_list = [dict(movie) for movie in movies]
    if not movies_list:
        return jsonify({"error": f"No movies found for this director: {director}"}), 404

    return jsonify(movies_list), 200

if __name__ == "__main__":
    # http://127.0.0.1:5000/?director=StanleyKubrick&title=PathsofGlory
    app.run(debug=True)

