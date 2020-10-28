from flask import Blueprint, render_template, redirect, url_for, request

import cs235flix.adapters.repository as repo
import cs235flix.genre.services as services
from cs235flix.utilities import utilities as utils

genre_blueprint = Blueprint('genre_bp', __name__, url_prefix='/genres')


# noinspection PyUnreachableCode,PyShadowingNames
@genre_blueprint.route('/', methods=['GET'])
def genre():
    """
    """
    search_form = utils.MovieSearchForm()
    genre = request.args.get('genre')
    if genre:
        try:
            movie_data = services.get_movies_by_genre(genre, repo.repo_instance)
            for movie in movie_data:
                movie['url'] = url_for('movie_bp.movie', title=movie['title'], year=movie['year'])
            movie_data.sort(key=lambda x: x['rank'])
            return render_template(
                'genre/genre.html',
                title=genre,
                watchlist=utils.get_user_watchlist(),
                movies=utils.get_added_movies(movie_data, utils.get_user_watchlist()),
                search_form=search_form,
            )
        except services.UnknownGenreException:
            return redirect(url_for('home_bp.home'))
        return redirect(url_for('home_bp.home'))
    else:
        return redirect(url_for('home_bp.home'))
