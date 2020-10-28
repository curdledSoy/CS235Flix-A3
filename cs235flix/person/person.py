from flask import Blueprint, render_template, redirect, url_for, request

import cs235flix.adapters.repository as repo
import cs235flix.person.services as services
from cs235flix.utilities import utilities as utils

person_blueprint = Blueprint(
    'person_bp', __name__, url_prefix='/people'
)


@person_blueprint.route('/director/', methods=['GET'])
def director():
    """
    """
    search_form = utils.MovieSearchForm()
    fullname = request.args.get('fullname')
    if fullname is not None:
        try:
            movie_data = services.get_movies_by_director(fullname, repo.repo_instance)
            for movie in movie_data:
                movie['url'] = url_for('movie_bp.movie', title=movie['title'], year=movie['year'])
            return render_template(
                'person/person.html',
                title="Director",
                fullname=fullname,
                watchlist=utils.get_user_watchlist(),
                movies=utils.get_added_movies(movie_data, utils.get_user_watchlist()),
                search_form=search_form
            )
        except ValueError:
            return render_template(redirect(url_for('home_bp.home')))
    return render_template(redirect(url_for('home_bp.home')))


@person_blueprint.route('/actor/')
def actor():
    """
    """
    search_form = utils.MovieSearchForm()
    fullname = request.args.get('fullname')
    if fullname:
        try:
            movie_data, collegues = services.get_movies_by_actor(fullname, repo.repo_instance)
            for movie in movie_data:
                movie['url'] = url_for('movie_bp.movie', title=movie['title'], year=movie['year'])
            for collegue in collegues:
                collegue['url'] = url_for('.actor', fullname=collegue['fullname'])
            return render_template(
                'person/person.html',
                title="Actor",
                fullname=fullname,
                watchlist=utils.get_user_watchlist(),
                movies=utils.get_added_movies(movie_data, utils.get_user_watchlist()),
                collegues=collegues,
                search_form=search_form,
            )
        except services.PersonException:
            return redirect(url_for('home_bp.home'))
    else:
        return redirect(url_for('home_bp.home'))
