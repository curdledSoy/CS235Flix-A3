from flask import Blueprint, render_template, url_for, request

import cs235flix.adapters.repository as repo
import cs235flix.browse.services as services
import cs235flix.utilities.utilities as utils
from cs235flix.cache import cache

browse_blueprint = Blueprint(
    'browse_bp', __name__, url_prefix='/browse'
)


# noinspection PyShadowingNames
@browse_blueprint.route('/directors')
def directors_by_inital():
    """
    """
    search_form = utils.MovieSearchForm()
    character = request.args.get('character')
    if character:
        directors = services.get_directors_by_first_letter(character, repo.repo_instance)
        for director in directors:
            director['url'] = url_for('person_bp.director', fullname=director['name'])
        return render_template(
            'browse/browse.html',
            title=f"Directors Starting With: {character}",
            data=directors,
            search_form=search_form,
        )
    else:
        letters = services.get_all_director_first_letter(repo.repo_instance)
        letter_urls = []
        for letter in letters:
            letter_urls.append(dict(letter=letter, url=url_for('.directors_by_inital', character=letter)))
        letter_urls.insert(0, dict(letter="All Directors", url=url_for('.directors')))
        return render_template(
            'browse/browse-a-z.html',
            title="Directors A-Z",
            a_to_z=letter_urls,
            search_form=search_form,
        )


# noinspection PyShadowingNames
@browse_blueprint.route('/directors/all')
def directors():
    """
    """
    search_form = utils.MovieSearchForm()
    directors = services.get_directors(repo.repo_instance)
    for director in directors:
        director['url'] = url_for('person_bp.director', fullname=director['name'])
    return render_template(
        'browse/browse.html',
        title="All Directors",
        data=directors,
        search_form=search_form,
    )


# noinspection PyShadowingNames
@browse_blueprint.route('/actors', methods=['GET'])
def actors_by_initial():
    """
    """
    search_form = utils.MovieSearchForm()
    character = request.args.get('character')
    if character:
        actors = services.get_actors_by_first_letter(character, repo.repo_instance)
        for actor in actors:
            actor['url'] = url_for('person_bp.actor', fullname=actor['name'])
        return render_template(
            'browse/browse.html',
            title=f"Actors Starting With: {character}",
            data=actors,
            search_form=search_form,
        )
    else:
        letters = services.get_all_actor_first_letter(repo.repo_instance)
        letter_urls = []
        for letter in letters:
            letter_urls.append(dict(letter=letter, url=url_for('.actors_by_initial', character=letter)))
        letter_urls.insert(0, dict(letter="All Actors", url=url_for('.actors')))
        return render_template(
            'browse/browse-a-z.html',
            title="Actors A-Z",
            a_to_z=letter_urls,
            search_form=search_form
        )


# noinspection PyShadowingNames
@browse_blueprint.route('/actors/all')
@cache.cached(timeout=50)
def actors():
    """
    """
    search_form = utils.MovieSearchForm()
    actors = services.get_actors(repo.repo_instance)
    for actor in actors:
        actor['url'] = url_for('person_bp.actor', fullname=actor['name'])
    return render_template(
        'browse/browse.html',
        title="All Actors",
        data=actors,
        search_form=search_form,
    )


# noinspection PyShadowingNames
@browse_blueprint.route('/genres')
def genres():
    """
    """
    genres = services.get_genres(repo.repo_instance)
    search_form = utils.MovieSearchForm()
    for genre in genres:
        genre['url'] = url_for('genre_bp.genre', genre=genre['name'])
    return render_template(
        'browse/browse.html',
        title='Genres',
        data=genres,
        search_form=search_form,
    )


# noinspection PyShadowingNames
@browse_blueprint.route('/movies', methods=['GET'])
def movies_by_first_letter():
    """
    """
    character = request.args.get('character')
    search_form = utils.MovieSearchForm()
    if character:
        movies = services.get_movies_by_first_letter(character, repo.repo_instance)
        for movie in movies:
            movie['url'] = url_for('movie_bp.movie', title=movie['title'], year=movie['year'])
        return render_template(
            'browse/browse-movies.html',
            title=f"Movies Starting With: {character}",
            watchlist=utils.get_user_watchlist(),
            movies=utils.get_added_movies(movies, utils.get_user_watchlist()),
            search_form=search_form
        )
    else:
        letters = services.get_all_movie_first_letter(repo.repo_instance)
        letter_urls = []
        for letter in letters:
            letter_urls.append(dict(letter=letter, url=url_for('.movies_by_first_letter', character=letter)))
        letter_urls.insert(0, dict(letter="All Movies", url=url_for('.movies')))
        return render_template(
            'browse/browse-a-z.html',
            title="Movies A-Z",
            a_to_z=letter_urls,
            search_form=search_form,
        )


# noinspection PyShadowingNames
@browse_blueprint.route('/movies/all')
def movies():
    """
    """
    search_form = utils.MovieSearchForm()
    movies = services.get_movies(repo.repo_instance)
    for movie in movies:
        movie['url'] = url_for('movie_bp.movie', title=movie['title'], year=movie['year'])
    return render_template(
        'browse/browse-movies.html',
        title='All Movies By Rank',
        watchlist=utils.get_user_watchlist(),
        movies=utils.get_added_movies(movies, utils.get_user_watchlist()),
        search_form=search_form
    )
