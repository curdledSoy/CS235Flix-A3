from cs235flix.domain.model import Director


class TestDirectorMethods:

    # noinspection PyTypeChecker
    def test_init(self):
        director1 = Director("Taika Waititi")
        assert repr(director1) == "<Director Taika Waititi>"
        director2 = Director("")
        assert director2.director_full_name is None
        director3 = Director(42)
        assert director3.director_full_name is None
        director4 = Director("Timothy Chalet")
        assert director1 < director4
