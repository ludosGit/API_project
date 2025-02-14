from models.genre import Genre
from models.movie import Movie

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

if __name__ == "__main__":
    print(MOVIES)