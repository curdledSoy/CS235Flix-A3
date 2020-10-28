import pytest
from cs235flix.domain.model import Genre


class TestGenreMethods:
    @pytest.fixture
    def genre(self):
        """
        """
        return Genre("Horror")

    def test_genre_name(self, genre):
        assert genre.genre_name == "Horror"
        assert Genre("").genre_name is None

    def test_repr(self, genre):
        assert repr(genre) == "<Genre Horror>"

    def test_eq(self, genre):
        assert genre == Genre("Horror")
        assert genre != Genre("Anthology")

    def test_lt(self, genre):
        assert Genre("Anthology") < genre
        assert genre < Genre("Kids Film")

    def test_hash(self, genre):
        assert hash(genre) == hash(Genre("Horror"))
        assert hash(genre) != hash(Genre("Kids Film"))
