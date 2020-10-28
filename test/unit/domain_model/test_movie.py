import pytest
from cs235flix.domain.model import Actor, Director, Genre, Movie, Review


class TestMovieMethods:
    @pytest.fixture
    def movie(self):
        """
        """
        mov = Movie("The 100", 2016)
        return mov

    def test_init(self, movie):
        assert movie == Movie("The 100", 2016)
        assert movie.description == ""
        assert movie.director is None
        assert movie.actors == []
        assert movie.genres == []
        assert movie.runtime_minutes == 0
        assert movie.rank is None
        assert movie.rating is None
        assert movie.votes is None
        assert movie.revenue is None
        assert movie.metascore is None

    def test_title(self, movie):
        movie.title = "Once Apon a Time"
        assert movie.title == "Once Apon a Time"

    def test_release_year(self, movie):
        assert movie.release_year == 2016

    def test_hash(self, movie):
        assert hash(movie) != hash(Movie("The 100", 2018))
        assert hash(movie) != hash(Movie("The 1000", 2016))

    def test_description(self, movie):
        movie.description = "This was a shit show"
        assert movie.description == "This was a shit show"

    def test_director(self, movie):
        movie.director = Director("Taika")
        assert movie.director == Director("Taika")

    def test_actors(self, movie):
        movie.add_actor(Actor("Tom"))
        assert movie.actors == [Actor("Tom")]

    def test_genres(self, movie):
        movie.add_genre(Genre("Thriller"))
        assert movie.genres == [Genre("Thriller")]

    def test_runtime_minutes(self, movie):
        movie.runtime_minutes = 109
        assert movie.runtime_minutes == 109

    def test_add_actor(self, movie):
        movie.add_actor(Actor('Tom'))

    def test_remove_actor(self, movie):
        movie.add_actor(Actor('Tom'))
        movie.add_actor(Actor('Jimmy'))
        movie.remove_actor(Actor('Tom'))
        assert movie.actors == [Actor('Jimmy')]
        movie.remove_actor(Actor("Tom Brittenden"))
        assert movie.actors == [Actor('Jimmy')]

    def test_add_genre(self, movie):
        genre = Genre("Horror")
        movie.add_genre(genre)
        assert movie.genres == [genre]

    def test_remove_genre(self, movie):
        genre1 = Genre("Horror")
        genre2 = Genre("Anthology")
        movie.add_genre(genre1)
        movie.add_genre(genre2)
        movie.remove_genre(genre1)
        assert movie.genres == [genre2]

    def test_eq(self, movie):
        assert movie == Movie("The 100", 2016)
        assert movie != Movie("The 1000", 2018)

    def test_lt(self, movie):
        assert movie < Movie("The 1000", 2016)
        assert movie > Movie("Bones", 2002)

    def test_add_review(self, movie):
        movie.add_review(Review)



