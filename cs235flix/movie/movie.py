from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, RadioField
from wtforms.validators import Length, InputRequired

import cs235flix.adapters.repository as repo
import cs235flix.movie.services as services
import cs235flix.utilities.utilities as utils
from cs235flix.authentication.authentication import login_required

movie_blueprint = Blueprint('movie_bp', __name__, url_prefix='/movies')


# noinspection PyUnreachableCode
@movie_blueprint.route('/', methods=['GET'])
def movie():
    """
    """
    title = request.args.get('title')
    year = request.args.get('year')
    search_form = utils.MovieSearchForm()
    try:
        movie_data = services.get_movie(title, year, repo.repo_instance)
        movie_data['add_review_url'] = url_for('movie_bp.review_movie', movie_title=movie_data['title'],
                                               movie_year=movie_data['year'])
        return render_template(
            'movie/movie.html',
            title="Movie",
            movie=utils.get_added_movies([movie_data], utils.get_user_watchlist())[0],
            search_form=search_form,
        )
    except services.UnknownMovieException:
        return redirect(url_for('home_bp.home'))
    return redirect(url_for('home_bp.home'))


# noinspection PyUnreachableCode,PyUnusedLocal
@movie_blueprint.route('/watch/', methods=['GET'])
@login_required
def watch():
    """
    """
    title = request.args.get('title')
    year = request.args.get('year')
    user = session['username']
    try:
        movie_data = services.watch_movie(user, title, year, repo.repo_instance)
        return redirect(url_for('movie_bp.movie', title=title, year=year))
    except services.UnknownMovieException:
        return redirect(request.referrer)
    return redirect(request.referrer)


# noinspection PyShadowingNames
@movie_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_movie():
    """
    """
    username = session['username']

    review_form = ReviewForm()
    search_form = utils.MovieSearchForm()
    if review_form.validate_on_submit():
        year = review_form.movie_year.data
        title = review_form.movie_title.data

        services.add_review(title, year, review_form.review.data, username, review_form.rating.data, repo.repo_instance)
        return redirect(url_for('movie_bp.movie', title=title, year=year))

    if request.method == 'GET':
        title = request.args.get('movie_title')
        year = request.args.get('movie_year')
        review_form.movie_year.data = year
        review_form.movie_title.data = title
    else:
        title = review_form.movie_title.data
        year = review_form.movie_year.data
    try:
        movie = services.get_movie(title, year, repo.repo_instance)
        return render_template(
            'movie/review_movie.html',
            movie_title=movie['title'],
            movie_year=movie['year'],
            review_form=review_form,
            search_form=search_form,
            handler_url=url_for('movie_bp.review_movie')
        )
    except:
        return redirect(url_for('movie_bp.movie', title=title, year=year))


class ReviewForm(FlaskForm):
    rating = RadioField('Rating', coerce=int, choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)],
                        validators=[InputRequired(message='Select a Rating Please')])
    review = TextAreaField('Review', [Length(min=5, message='Your Review isn\'t big enough 😔')])
    movie_year = HiddenField()
    movie_title = HiddenField()
    submit = SubmitField('Add Review')
