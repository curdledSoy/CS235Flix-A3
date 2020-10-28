from fuzzywuzzy import process

import cs235flix.utilities.utilities as utils
from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import Actor, Director, Genre


def get_actors(repo: AbstractRepository):
    """
    """
    actors = sorted(repo.dataset_of_actors)

    return [(actor.actor_full_name, actor.actor_full_name) for actor in actors]


def get_directors(repo: AbstractRepository):
    """
    """
    directors = sorted(repo.dataset_of_directors)
    return [(None, None)] + [(director.director_full_name, director.director_full_name) for director in directors]


def get_genres(repo: AbstractRepository):
    """
    """
    genres = sorted(repo.dataset_of_genres)
    return [(genre.genre_name, genre.genre_name) for genre in genres]


def get_search_results(actors, genres, director, fuzzy, repo: AbstractRepository):
    """
    """
    results = [utils.movie_to_dict(movie) for movie in repo.dataset_of_movies]
    if actors:
        actor_movies = get_movies_for_actors(actors, repo)
        results = [movie for movie in results if movie in actor_movies]
    if genres:
        genre_movies = get_movies_for_genres(genres, repo)
        results = [movie for movie in results if movie in genre_movies]
    if director and director != 'None':
        director_movies = get_movies_for_director(director, repo)
        results = [movie for movie in results if movie in director_movies]
    if fuzzy:
        fuzzy_search_results = get_fuzzy_search_movies(fuzzy, repo)
        results = [movie for movie in results if movie in fuzzy_search_results]
    return sorted(results, key=lambda x: x['rank'])


def get_fuzzy_search_movies(fuzzy, repo):
    """
    """
    movies = list(repo.dataset_of_movies)
    movie_title_dict = dict(enumerate([movie.title for movie in movies]))
    best_matches = process.extractBests(fuzzy, movie_title_dict, score_cutoff=50)
    return [utils.movie_to_dict(movie) for movie in [movies[z] for (x, y, z) in best_matches]]


def get_movies(actors, genres, director, repo: AbstractRepository):
    """
    """
    movies = repo.dataset_of_movies
    matches = set()
    for movie in movies:
        for actor in actors:
            if actor in [actor.actor_full_name for actor in movie.actors]:
                if len(genres) > 0:
                    for genre in genres:
                        if genre in [genre.genre_name for genre in movie.genres]:
                            if director is not None:
                                if director == movie.director.director_full_name:
                                    matches.add(movie)
                                else:
                                    if movie in matches:
                                        matches.remove(movie)
                            else:
                                matches.add(movie)
                        else:
                            if movie in matches:
                                matches.remove(movie)
            else:
                if movie in matches:
                    matches.remove(movie)
    return [utils.movie_to_dict(movie) for movie in matches]


def get_movies_for_director(director, repo):
    """
    """
    if director is None:
        return []
    return [utils.movie_to_dict(movie) for movie in repo.get_movies_by_director(Director(director))]


def get_movies_for_genres(genres, repo):
    """
    """
    movies = set()
    to_remove = []
    for genre in genres:
        genre_obj = Genre(genre)
        for movie in repo.get_movies_by_genre(genre_obj):
            movies.add(movie)
    for genre in genres:
        genre_obj = Genre(genre)
        for movie in movies:
            if genre_obj not in movie.genres:
                to_remove.append(movie)
    for item in to_remove:
        movies.remove(item)
    return [utils.movie_to_dict(movie) for movie in movies]


def get_movies_for_actors(actors, repo):
    """
    """
    movies = set()
    to_remove = []
    for actor in actors:
        actor_obj = Actor(actor)
        for movie in repo.get_movies_by_actor(actor_obj):
            movies.add(movie)

    for actor in actors:
        actor_obj = Actor(actor)
        for movie in movies:
            if actor_obj not in movie.actors:
                to_remove.append(movie)
    for item in to_remove:
        if item in movies:
            movies.remove(item)
    return [utils.movie_to_dict(movie) for movie in movies]
