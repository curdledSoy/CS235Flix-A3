import pytest
from cs235flix.domain.model import Actor


class TestActorMethods:
    @pytest.fixture
    def actor1(self):
        """
        """
        actor = Actor("Lindsay Lohan")
        return actor

    @pytest.fixture
    def actor2(self):
        """
        """
        actor = Actor("Brad Pitt")
        return actor

    @pytest.fixture
    def actor3(self):
        """
        """
        actor = Actor("")
        return actor

    def test_actor_full_name(self, actor1, actor2, actor3):
        assert actor1.actor_full_name == "Lindsay Lohan"
        assert actor2.actor_full_name == "Brad Pitt"
        assert actor3.actor_full_name is None

    def test_add_actor_colleague(self, actor1, actor2):
        actor1.add_actor_colleague(actor2)
        assert actor2.check_if_this_actor_worked_with(actor1)

    def test_check_if_this_actor_worked_with(self, actor1, actor2):
        assert not actor1.check_if_this_actor_worked_with(actor2)
        assert not actor2.check_if_this_actor_worked_with(actor1)

    def test_eq(self, actor1, actor2):
        assert actor1 != actor2
        assert actor1 == Actor("Lindsay Lohan")

    def test_lt(self, actor1, actor2):
        assert actor1 > actor2
        assert not actor2 > actor1

    def test_hash(self, actor1, actor2):
        assert hash(actor1) != hash(actor2)

    def test_repr(self, actor1, actor2, actor3):
        assert repr(actor1) == "<Actor Lindsay Lohan>"
        assert repr(actor2) == "<Actor Brad Pitt>"
        assert repr(actor3) == "<Actor None>"
