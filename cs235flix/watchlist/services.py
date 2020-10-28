import cs235flix.utilities.utilities as utils
from cs235flix.adapters.repository import AbstractRepository


def get_user_watchlist(username: str, repo: AbstractRepository):
    """
    """
    watchlist = repo.get_watchlists_for_user(repo.get_user(username=username))
    if watchlist and watchlist.size() != 0:
        return [utils.movie_to_dict(movie) for movie in watchlist]
    else:
        return []


def add_to_watchlist(username: str, title: str, year: str, repo: AbstractRepository):
    """
    """
    user = repo.get_user(username)
    if user:
        movie = repo.get_movie(title, int(year))
        if movie:
            repo.add_movie_to_watchlist(user, movie)


def remove_from_watchlist(username: str, title: str, year: str, repo: AbstractRepository):
    """
    """
    user = repo.get_user(username)
    if user:
        movie = repo.get_movie(title, int(year))
        if movie:
            repo.remove_movie_from_watchlist(user, movie)
