from datetime import date, datetime
from typing import List


import pytest

from cs235flix.domain.model import User, Movie, Review, Actor, Director, Genre, WatchList, make_review
from cs235flix.adapters.repository import RepositoryException


def test_repo_can_add_user(in_memory_repo):
    user = User('tom', '1234')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('tom') is user


def test_repo_can_get_user(in_memory_repo):
    user = in_memory_repo.get_user('admin')
    assert user == User('admin', 'admin')

def test_repo_cant_get_unknown_user(in_memory_repo):
    user = in_memory_repo.get_user('Sophie')
    assert user is None

def test_repo_can_get_movie(in_memory_repo):
    movie = in_memory_repo.get_movie('Moana', 2016)
    assert movie == Movie('Moana', 2016)

def test_repo_can_add_movie(in_memory_repo):
    movie = Movie('Tom', 2001)
    movie.director = Director('Tom')
    movie.actors = [Actor('Tom')]
    movie.runtime_minutes = 20
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie('Tom', 2001) == movie

def test_repo_cant_get_fake_movie(in_memory_repo):
    movie = in_memory_repo.get_movie('abcsdfsjfkls', 2024)
    assert movie == None


def test_repo_can_get_reviews(in_memory_repo):
    review = in_memory_repo.get_reviews()

    assert review == []

def test_repo_can_add_review(in_memory_repo):
    movie = in_memory_repo.get_movie('Moana', 2016)
    user = in_memory_repo.get_user('admin')
    review = make_review(user, movie, 'Cool', 5)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()

def test_repo_wont_add_invalid_review(in_memory_repo):
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(Review(None, None, 2345, 'a'))

def test_repo_can_add_actor(in_memory_repo):
    actor = Actor('Tom')
    in_memory_repo.add_actor(actor)
    assert in_memory_repo.get_actor('Tom') == actor

def test_repo_wont_get_unreal_actor(in_memory_repo):
    assert in_memory_repo.get_actor(5) == None

def test_repo_wont_add_invalid_actor(in_memory_repo):
    with pytest.raises(RepositoryException):
        in_memory_repo.add_actor(Actor(1))

def test_repo_can_add_director(in_memory_repo):
    director = Director('Tom')
    in_memory_repo.add_director(director)
    assert in_memory_repo.get_director_by_name('Tom') == director

def test_repo_wont_get_unreal_director(in_memory_repo):
    assert in_memory_repo.get_director_by_name('!') == None

def test_repo_wont_add_invalid_director(in_memory_repo):
    with pytest.raises(RepositoryException):
        in_memory_repo.add_director(Director(1))

def test_repo_can_add_genre(in_memory_repo):
    genre = Genre('Tom')
    in_memory_repo.add_genre(genre)
    assert in_memory_repo.get_genre('Tom') == genre

def test_repo_wont_get_unreal_genre(in_memory_repo):
    assert in_memory_repo.get_genre(0) == None










