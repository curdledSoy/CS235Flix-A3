from werkzeug.security import generate_password_hash, check_password_hash

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import User


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class NameNotUnqiueException(Exception):
    pass


def add_user(username: str, password: str, repo: AbstractRepository):
    """
    """
    user = repo.get_user(username)
    if user:
        raise NameNotUnqiueException

    password_hash = generate_password_hash(password)

    repo.add_user(User(username, password_hash))


def get_user(username: str, repo: AbstractRepository):
    """
    """
    user = repo.get_user(username)
    if not user:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    """
    """
    authenticated = False

    user = repo.get_user(username)
    if user:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def user_to_dict(user: User):
    """
    """
    return {'username': user.user_name, 'password': user.password}
