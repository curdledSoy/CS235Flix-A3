from flask import Blueprint, render_template, session, redirect, request

import cs235flix.adapters.repository as repo
import cs235flix.utilities.utilities as utils
import cs235flix.watchlist.services as services
from cs235flix.authentication.authentication import login_required

watchlist_blueprint = Blueprint(
    'watchlist_bp', __name__, url_prefix='/watchlist'
)


@watchlist_blueprint.route('/')
@watchlist_blueprint.route('')
@login_required
def watchlist():
    """
    """
    return render_template(
        'watchlist/watchlist.html',
        title='Watchlist',
        watchlist=utils.get_user_watchlist(),
        search_form=utils.MovieSearchForm(),
    )


# noinspection PyTypeChecker
@watchlist_blueprint.route('/add/')
@login_required
def add_to_watchlist():
    """
    """
    title = request.args.get('title')
    year = request.args.get('year')
    services.add_to_watchlist(session['username'], title, int(year), repo.repo_instance)
    return redirect(request.referrer)


# noinspection PyTypeChecker
@watchlist_blueprint.route('/remove')
@login_required
def remove_from_watchlist():
    """
    """
    title = request.args.get('title')
    year = request.args.get('year')
    services.remove_from_watchlist(session['username'], title, int(year), repo.repo_instance)
    return redirect(request.referrer)
