import pytest
from cs235flix.domain.model import Movie, User, UserGroup


class TestUserGroupMethods:
    @pytest.fixture
    def user(self):
        """
        """
        return User("Tom Brittenden", "123")

    @pytest.fixture
    def usergroup(self, user):
        """
        """
        return UserGroup(user)

    def test_construction(self, user, usergroup):
        assert usergroup.members == [user]
        assert usergroup.owner == user
        assert usergroup.group_name == "New Group"

    def test_watch_movie(self, usergroup):
        mov = Movie("Moana", 2016)
        mov.runtime_minutes = 20
        usergroup.watch_movie(mov)
        for user in usergroup.members:
            assert user.time_spent_watching_movies_minutes == 20

    # noinspection PyTypeChecker
    def test_add_member(self, usergroup, user):
        usergroup.add_member(User("Sophie", "abc"))
        assert usergroup.members == [user, User("Sophie", "abc")]
        usergroup.add_member(User("Sophie", "abc"))
        usergroup.add_member("Hi")
        assert usergroup.members == [user, User("Sophie", "abc")]

    # noinspection PyTypeChecker
    def test_remove_member(self, usergroup, user):
        usergroup.add_member(User("Sophie", "abc"))
        usergroup.add_member(User("Tim", "ab3"))
        usergroup.remove_member(User("Sophie", "abc"))
        assert usergroup.members == [user, User("Tim", "ab3")]
        usergroup.remove_member(User("Sophie", "abc"))
        assert usergroup.members == [user, User("Tim", "ab3")]
        usergroup.remove_member('a')
        assert usergroup.members == [user, User("Tim", "ab3")]
