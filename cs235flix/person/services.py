import cs235flix.utilities.utilities as utils
from cs235flix.adapters.repository import AbstractRepository
from cs235flix.cache import cache
from cs235flix.domain.model import Actor


class PersonException(Exception):
    pass


@cache.memoize(timeout=30)
def get_movies_by_director(director: str, repo: AbstractRepository):
    """
    """
    director = repo.get_director_by_name(director)
    if director is None:
        raise PersonException
    movies = repo.get_movies_by_director(director)
    return [utils.movie_to_dict(movie) for movie in sorted(movies, key=lambda x: x.rank)]


@cache.memoize(timeout=30)
def get_collegues(actor: Actor):
    """
    """
    collegues = []
    for collegue in actor.has_worked_with:
        collegues.append(dict(fullname=collegue.actor_full_name))
    return collegues


@cache.memoize(timeout=30)
def get_movies_by_actor(actor, repo: AbstractRepository):
    """
    """
    actor = repo.get_actor(actor)
    if actor is None:
        raise PersonException('Actor does not exist')
    movies = repo.get_movies_by_actor(actor)
    return [utils.movie_to_dict(movie) for movie in sorted(movies, key=lambda x: x.rank)], get_collegues(actor)
