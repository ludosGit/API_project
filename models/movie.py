# Pydantic is a data validation and settings management library for Python,
# which uses Python type annotations to validate and serialize data. Features:
# Data Validation: Ensures the data matches the expected types.
# Automatic Type Conversion: Converts compatible types automatically (e.g., str to int).
# Schema Generation: Can generate JSON Schema from models.
# Nested Models: Supports complex, hierarchical data structures.
# Performance Optimized: Built on top of dataclasses and Cython for efficiency.
# Environment Variables Handling: Ideal for configuration management.
# Custom Validators: Allows defining custom validation logic.

from pydantic import BaseModel
from datetime import datetime
from models.genre import Genre

class Movie(BaseModel):
    genre: Genre
    title: str
    rating: int
    comment: str
    director: str
    year: int
    views: list[str]
    image: str = None

    def json(self):
        if self.image:
            return {
                "title": self.title,
                "genre": self.genre.value,  # Use the .value of the Enum
                "rating": self.rating,
                "comment": self.comment,
                "director": self.director,
                "year": self.year,
                "views": self.views,
                "image": self.image
            }
        else:
            return {
                "title": self.title,
                "genre": self.genre.value,  # Use the .value of the Enum
                "rating": self.rating,
                "comment": self.comment,
                "director": self.director,
                "year": self.year,
                "views": self.views,
            }

if __name__ == "__main__":
    movie = Movie(genre=Genre.COMEDY, title="The Hangover", rating=5, comment="Hilarious movie!", director="Todd Phillips", year=2009, views=['2021-10-15'])
    print(movie)
    print(movie.model_json_schema())
