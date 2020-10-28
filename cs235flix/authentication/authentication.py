from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import cs235flix.adapters.repository as repo
import cs235flix.authentication.services as services
import cs235flix.utilities.utilities as utils

authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/auth')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    """
    auth_form = RegistrationForm()
    search_form = utils.MovieSearchForm()
    username_unique = None

    if auth_form.validate_on_submit():
        try:
            services.add_user(auth_form.username.data, auth_form.password.data, repo.repo_instance)
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUnqiueException:
            username_unique = "Username is already used, please try another one"
            return render_template(
                'authentication/credentials.html',
                title='Register',
                auth_form=auth_form,
                username_error_message=username_unique,
                handler_url=url_for('authentication_bp.register'),
                search_form=search_form
            )
    return render_template(
        'authentication/credentials.html',
        title='Register',
        auth_form=auth_form,
        username_error_message=username_unique,
        handler_url=url_for('authentication_bp.register'),
        search_form=search_form
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    """
    auth_form = LoginForm()
    search_form = utils.MovieSearchForm()
    username_not_recognised = None
    password_doesnt_match = None
    if auth_form.validate_on_submit():
        try:
            user = services.get_user(auth_form.username.data, repo.repo_instance)
            services.authenticate_user(user['username'], auth_form.password.data, repo.repo_instance)

            session.clear()
            session['username'] = user['username']
            return redirect(url_for('home_bp.home'))
        except services.UnknownUserException:
            username_not_recognised = "Username not recognised- please try another"
        except services.AuthenticationException:
            password_doesnt_match = 'Password does not match username. Please examine your credentials and try again'

    return render_template(
        'authentication/credentials.html',
        title='Login',
        username_error_message=username_not_recognised,
        password_error_message=password_doesnt_match,
        auth_form=auth_form,
        search_form=search_form,
    )


@authentication_blueprint.route('/logout')
def logout():
    """
    """
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    """
    """
    @wraps(view)
    def wrapped_view(**kwargs):
        """
        """
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)

    return wrapped_view


class PasswordValid:
    """
    """
    def __init__(self, message=None):
        if not message:
            message = u"Your password must contain an uppercase letter, a lowercase letter, a digit and be at least 6 "\
                      u"characters in length "
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(6) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [DataRequired(message="Your username is required"),
                                        Length(min=3, message="Username too short!")],
                           render_kw={"placeholder": "Username"}
                           )
    password = PasswordField('Password', [DataRequired(message="Your password is required"),
                                          PasswordValid()],
                             render_kw={"placeholder": "Password"},
                             )

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', [DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')
