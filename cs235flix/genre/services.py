import cs235flix.utilities.utilities as utils
from cs235flix.adapters.repository import AbstractRepository


class UnknownGenreException(Exception):
    pass


def get_movies_by_genre(genre: str, repo: AbstractRepository):
    """
    """
    genre = repo.get_genre(genre)
    if genre is None:
        raise UnknownGenreException
    movies = repo.get_movies_by_genre(genre)

    return [utils.movie_to_dict(movie) for movie in movies]





