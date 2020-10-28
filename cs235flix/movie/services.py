import cs235flix.utilities.utilities as utils
from cs235flix.adapters.repository import AbstractRepository
from cs235flix.authentication.services import UnknownUserException
from cs235flix.domain.model import make_review


class UnknownMovieException(Exception):
    pass


def get_movie(title: str, year: str, repo: AbstractRepository):
    """
    """
    try:
        movie = repo.get_movie(title, int(year))
        if not movie:
            raise UnknownMovieException
        return utils.movie_to_dict(movie)
    except:
        pass


def add_review(title: str, year: str, review_text: str, username: str, rating: int, repo: AbstractRepository):
    """
    """
    movie = repo.get_movie(title, int(year))
    if movie is None:
        raise UnknownMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    review = make_review(user, movie, review_text, rating)
    repo.add_review(review)


def watch_movie(username: str, title: str, year: str, repo: AbstractRepository):
    """
    """
    movie = repo.get_movie(title, int(year))
    if movie:
        user = repo.get_user(username)
        if user:
            user.watch_movie(movie)
