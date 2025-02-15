# An Enum (Enumeration) is a class in Python that defines a set of named constant values.
# It helps in organizing related constants, making code more readable and maintainable.

from enum import Enum

class Genre(Enum):
    COMEDY = "comedy"
    DRAMA = "drama"
    ACTION = "action"
    HORROR = "horror"
    THRILLER = "thriller"
    WAR = "war"
    ANIME = "anime"