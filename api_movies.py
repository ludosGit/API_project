import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from movies_db import MOVIES
from models.movie import Movie
from models.genre import Genre

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
    views = data.get('views')
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
        views=[v for v in views]
    )
 
    MOVIES.append(movie_entry)
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
    return jsonify([m.json() for m in MOVIES]), 200

@app.route('/mymovies/<genre>', methods=['GET'])
def get_movies_by_genre(genre):
    """Endpoint to retrieve movies by genre."""
    filtered_movies = [m for m in MOVIES if m.genre.value.lower() == genre.lower()]
    if not filtered_movies:
        return jsonify({"error": "No movies found for this genre"}), 404

    return jsonify([m.json() for m in filtered_movies])

@app.route('/mymovies/genres', methods=['GET'])
def get_all_genres():
    """Endpoint to retrieve all genres."""
    return jsonify([genre.value for genre in Genre]), 200

@app.route("/mymovies/directors/<string:director>", methods=["GET"])
def get_movies_by_director(director):
    filtered_movies = [m for m in MOVIES if m.director.lower().replace(" ", "") == director.lower()]
    if not filtered_movies:
        return jsonify({"error": "No movies found for this director"}), 404

    return jsonify([m.json() for m in filtered_movies])

@app.route("/mymovies/directors/<string:director>/<string:title>", methods=["GET"])
def get_movie_by_title(director, title):
    movie = next((m for m in MOVIES if m.director.lower().replace(" ", "") == director.lower() and m.title.lower().replace(" ", "") == title.lower()), None)
    print(movie)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    return jsonify(movie.json())

if __name__ == "__main__":
    # http://127.0.0.1:5000/?director=StanleyKubrick&title=PathsofGlory
    app.run(debug=True)

