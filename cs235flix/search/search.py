from flask import Blueprint, render_template, redirect, url_for, request

import cs235flix.adapters.repository as repo
import cs235flix.search.services as services
import cs235flix.utilities.utilities as utils

search_bp = Blueprint(
    'search_bp', __name__, url_prefix='/search'
)


@search_bp.route('', methods=['GET', 'POST'])
@search_bp.route('/', methods=['GET', 'POST'])
def search():
    """
    """
    search_form = utils.MovieSearchForm(request.form)
    search_form.actors.choices = services.get_actors(repo.repo_instance)
    search_form.director.choices = services.get_directors(repo.repo_instance)
    search_form.genres.choices = services.get_genres(repo.repo_instance)
    if request.method == 'POST':
        if search_form.validate_on_submit():
            return search_results(search_form)
        else:
            return redirect(url_for('.search', ))
    else:
        request.form = search_form
        return render_template('search/search.html', search_form=search_form, title="Search")


@search_bp.route('/search/results')
def search_results(search_form):
    """
    """
    movies = services.get_search_results(search_form.actors.data, search_form.genres.data,
                                         search_form.director.data, search_form.fuzzy.data,
                                         repo.repo_instance)
    for movie in movies:
        movie['url'] = url_for('movie_bp.movie', title=movie['title'], year=movie['year'])
    return render_template(
        'search/results.html',
        search_form=search_form,
        title="Search",
        watchlist=utils.get_user_watchlist(),
        movies=utils.get_added_movies(movies, utils.get_user_watchlist()),
    )
