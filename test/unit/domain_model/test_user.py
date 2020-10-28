import pytest
from cs235flix.domain.model import Movie, Review, User


class TestUserMethods:
    @pytest.fixture
    def user(self):
        """
        """
        return User("tombrittenden", "123")

    @pytest.fixture
    def movie(self):
        """
        """
        return Movie("Moana", 2016)

    # noinspection PyTypeChecker,PyTypeChecker
    def test_construction(self):
        user2 = User(1, 2)
        assert user2.user_name is None
        assert user2.password is None
        assert user2.watched_movies == []
        assert user2.time_spent_watching_movies_minutes == 0
        assert user2.reviews == []

    def test_watch_movie(self, user, movie):
        movie.runtime_minutes = 101
        user.watch_movie(movie)
        assert user.time_spent_watching_movies_minutes == 101
        assert user.watched_movies == [movie]

    # noinspection PyArgumentList
    def test_add_review(self, user, movie):
        review = Review(movie, user,"good movies", 8)
        user.add_review(review)
        assert user.reviews == [review]

    def test_repr(self, user):
        assert repr(user) == "<User tombrittenden>"

    def test_eq(self, user):
        assert user == User("Tombrittenden", "")
        assert user == User("TomBrittenden", "")
        assert user == User("TombrittendeN", "")
        assert user == User("TOMBRITTENDEN", "")
        assert user != User("Tim", " ")

    def test_lt(self, user):
        assert user > User("Sophie", "")
        assert user < User("VioletA12", "flowers1234!")
