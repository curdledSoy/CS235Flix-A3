from flask import Blueprint, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import Optional, Length

import cs235flix.adapters.repository as repo
import cs235flix.domain.model as model
import cs235flix.utilities.services as services

utilities_bp = Blueprint(
    'utilities_bp', __name__)


def get_user_watchlist():
    """
    """
    if 'username' in session:
        user_watchlist = services.get_user_watchlist(username=session['username'], repo=repo.repo_instance)
        for movie in user_watchlist:
            movie['url'] = url_for('movie_bp.movie', title=movie['title'], year=movie['year'])
        return user_watchlist


def movie_to_dict(movie: model.Movie):
    """
    """
    movie_dict = dict(rank=ordinal(movie.rank), title=movie.title, year=movie.release_year,
                      runtime=movie.runtime_minutes,
                      actors=[actor.actor_full_name for actor in movie.actors],
                      director=movie.director.director_full_name, genres=[genre.genre_name for genre in movie.genres],
                      description=movie.description, rating=movie.rating, votes=movie.votes, revenue=movie.revenue,
                      meta_score=movie.metascore, reviews=reviews_to_dict(movie.reviews))
    return movie_dict


def reviews_to_dict(reviews):
    """
    """
    return sorted([services.review_to_dict(review) for review in reviews], reverse=True, key=lambda x: x['timestamp'])


def get_added_movies(movies, watchlist):
    """
    """
    for item1 in movies:
        if watchlist:
            for item2 in watchlist:
                if item1['title'] == item2['title'] and item1['year'] == item2['year']:
                    item1['added'] = True
    return movies


def ordinal(n):
    """
    """
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


def _add_chosen_class(kwargs):
    """
    Add the class 'chosen-select' to the HTML elements, keeping any
    other specified render parameters or other classes.
    """
    if 'render_kw' in kwargs:
        if 'class' in kwargs['render_kw']:
            kwargs['render_kw']['class'] += ' chosen-select'
        else:
            kwargs['render_kw']['class'] = 'chosen-select'
    else:
        kwargs['render_kw'] = {'class': 'chosen-select'}


class ChosenSelectField(SelectField):
    """
    """
    def __init__(self, *args, **kwargs):
        _add_chosen_class(kwargs)
        super(ChosenSelectField, self).__init__(*args, **kwargs)


class ChosenSelectMultipleField(SelectMultipleField):
    """
    """
    def __init__(self, *args, **kwargs):
        _add_chosen_class(kwargs)
        super(ChosenSelectMultipleField, self).__init__(*args, **kwargs)


class MovieSearchForm(FlaskForm):
    actors = ChosenSelectMultipleField('Filter Movies by Actors', validators=[Optional()])
    director = ChosenSelectField('Filter Movies by Directors', validators=[Optional()])
    genres = ChosenSelectMultipleField('Filter Movies by Genres', validators=[Optional()])
    fuzzy = StringField('Search Movie by Name', validators=[Optional(), Length(min=2)],
                        render_kw={"placeholder": "Search for Movies"})
    submit = SubmitField('Search')

    def any_fields_filled(self):
        """
        """
        return any([self.actors.data, self.director.data, self.genres.data, self.fuzzy.data])

    def validate(self):
        """
        """
        return self.any_fields_filled()
