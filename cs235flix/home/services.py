import cs235flix.utilities.utilities as utils
from cs235flix.adapters.repository import AbstractRepository


def get_top_100movies(repo: AbstractRepository):
    """
    """
    movies = repo.get_movies_by_rank()[0:100]

    return [utils.movie_to_dict(movie) for movie in movies]
