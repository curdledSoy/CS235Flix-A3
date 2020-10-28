import cs235flix.utilities.utilities as utils
from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import User


def get_user(username, repo: AbstractRepository):
    """
    """
    user = repo.get_user(username)
    if user:
        return user_to_dict(user)
    else:
        return None


# noinspection PyUnusedLocal
def user_to_dict(user: User):
    """
    """
    user_dict = dict(
        username=user.user_name,
        watchlist=utils.get_user_watchlist(),
        watched_movies=[utils.movie_to_dict(movie) for movie in user.watched_movies],
        reviews=utils.reviews_to_dict(user.reviews),
        time_spent=user.time_spent_watching_movies_minutes,
        isAdmin=user.is_admin,
    )
