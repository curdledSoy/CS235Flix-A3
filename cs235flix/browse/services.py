import cs235flix.utilities.utilities as utils
from cs235flix.adapters.repository import AbstractRepository
from cs235flix.cache import cache


class BrowseException(Exception):
    pass


def get_genres(repo: AbstractRepository):
    """
    """
    genres = []
    for genre in sorted(repo.dataset_of_genres):
        movies = repo.get_movies_by_genre(genre)
        genres.append(dict(name=genre.genre_name, movies=[utils.movie_to_dict(movie) for movie in movies]))
    return genres


@cache.memoize(timeout=30)
def get_actors(repo: AbstractRepository):
    """
    """
    actors = []
    for actor in sorted(repo.dataset_of_actors):
        movies = repo.get_movies_by_actor(actor)
        actors.append(dict(name=actor.actor_full_name, movies=[utils.movie_to_dict(movie) for movie in movies]))
    return actors


@cache.memoize(timeout=30)
def get_actors_by_first_letter(character: str, repo: AbstractRepository):
    """
    """
    matching_actors = []
    for actor in sorted(repo.dataset_of_actors):
        if actor.actor_full_name[0] == character.upper():
            movies = repo.get_movies_by_actor(actor)
            matching_actors.append(
                dict(name=actor.actor_full_name, movies=[utils.movie_to_dict(movie) for movie in movies]))
    return matching_actors


@cache.memoize(timeout=30)
def get_all_actor_first_letter(repo: AbstractRepository):
    """
    """
    actor_names = sorted([actor.actor_full_name for actor in repo.dataset_of_actors])
    first_letters = []
    for name in actor_names:
        if name[0] not in first_letters:
            first_letters.append(name[0])
    first_letters.sort()
    return first_letters


@cache.memoize(timeout=30)
def get_directors_by_first_letter(character: str, repo: AbstractRepository):
    """
    """
    matching_directors = []
    for director in sorted(repo.dataset_of_directors):
        if director.director_full_name[0] == character.upper():
            movies = repo.get_movies_by_director(director)
            matching_directors.append(
                dict(name=director.director_full_name, movies=[utils.movie_to_dict(movie) for movie in movies]))
    return matching_directors


@cache.memoize(timeout=30)
def get_all_director_first_letter(repo: AbstractRepository):
    """
    """
    director_names = sorted([director.director_full_name for director in repo.dataset_of_directors])
    first_letters = []
    for name in director_names:
        if name[0] not in first_letters:
            first_letters.append(name[0])
    first_letters.sort()
    return first_letters


@cache.memoize()
def get_directors(repo: AbstractRepository):
    """
    """
    directors = []
    for director in sorted(repo.dataset_of_directors):
        movies = repo.get_movies_by_director(director)
        directors.append(dict(movies=movies, name=director.director_full_name))
    return directors


@cache.memoize()
def get_movies_by_director(director: str, repo: AbstractRepository):
    """
    """
    director = repo.get_director_by_name(director)
    if director is None:
        raise BrowseException
    movies = repo.get_movies_by_director(director)
    return [utils.movie_to_dict(movie) for movie in movies]


@cache.memoize(timeout=30)
def get_movies_by_first_letter(character: str, repo: AbstractRepository):
    """
    """
    matching_movies = []
    for movie in sorted(repo.dataset_of_movies):
        if movie.title[0] == character.upper():
            matching_movies.append(utils.movie_to_dict(movie))
    return matching_movies


@cache.memoize(timeout=30)
def get_all_movie_first_letter(repo: AbstractRepository):
    """
    """
    movie_names = [movie.title for movie in sorted(repo.dataset_of_movies)]
    first_letters = []
    for name in movie_names:
        if name[0] not in first_letters:
            first_letters.append(name[0])
    first_letters.sort()
    return first_letters


def get_movies(repo: AbstractRepository):
    """
    """
    return [utils.movie_to_dict(movie) for movie in sorted(repo.dataset_of_movies, key=lambda x: x.rank)]
