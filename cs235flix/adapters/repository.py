import abc
from datetime import date
from typing import List

from cs235flix.domain.model import User, Movie, Director, Genre, UserGroup, Actor, Review, WatchList

repo_instance = None


class RepositoryException(Exception):
    """
    """

    # noinspection PyUnusedLocal
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @property
    @abc.abstractmethod
    def dataset_of_movies(self):
        """
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def dataset_of_actors(self):
        """
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def dataset_of_directors(self):
        """
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def dataset_of_genres(self):
        """
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def dataset_of_users(self):
        """
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def dataset_of_groups(self):
        """
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def dataset_of_reviews(self):
        """
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def dataset_of_watchlists(self):
        """
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """Adds User to the Repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """Returns the User Object that matches username Argument, otherwise none"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """
        Adds Movie Object to Repository, if any properties which estabilish a bi-directional link fails,
        raise a RepositoryException and dont update repo
        """
        if not movie.director:
            raise RepositoryException('Movie cannot be added to repository: Director is None')
        if not movie.actors:
            raise RepositoryException('Movie cannot be added to repository: Actors is Empty')
        if movie.runtime_minutes < 0:
            raise RepositoryException('Movie cannot be added to repository: Runtime is 0')

    @abc.abstractmethod
    def get_movie(self, title: str, year: int) -> Movie:
        """Returns Movie Object that matches title and year argument
        If No Object matches the parameters, return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_year(self, target_year: date) -> List[Movie]:
        """Returns List of Movies released in the target_year argument
        If no Movies were released in this year, return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_title(self, title: str) -> List[Movie]:
        """
        Returns List of Movie Objects that match the title argument
        If no Movie Objects match this title, Return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, director: Director) -> List[Movie]:
        """
        Returns List of Movie Objects that match the director argument
        If no Movie Objects match this director, return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, actor: Actor) -> List[Movie]:
        """
        Returns a List of Movie Objects that contain the Actor object argument
        If no Movie objects contain this Actor object, return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, genre: Genre) -> List[Movie]:
        """
        Returns a List of Movie Objects that contain the Genre object argument.
        If no Movie objects contain this Genre object, return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_rating(self, rating: int) -> List[Movie]:
        """
        Returns a List of Movie Objects where the rating attribute(s) is greater than or equal
        to the rating parameter passed to this function.
        If no Movie Objects contain this rating attribute, then return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_rank(self) -> List[Movie]:
        """
        Returns a List of Movie Objects, their position in this list determined by their rank attributes.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_group(self, group: UserGroup):
        """
        Adds a User Group to the Repositiory
        """
        if not group.owner:
            raise RepositoryException('UserGroup cannot be added to Repository: No Owner attached')

    @abc.abstractmethod
    def get_group(self, groupname) -> UserGroup:
        """
        Returns UserGroup object where this objects groupname attribute is the same as groupname argument
        Otherwise returns none.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_groups(self, user: User) -> List[UserGroup]:
        """
        Returns List of UserGroup Objects that the user parameter object is a member of.
        If the User object is not a member of any groups return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """
        Adds Review to Repository if review is set up properly, otherwise raises a RepositoryException and doesnt add
        to repo.
        """
        if review.movie is None:
            raise RepositoryException("Review cannot be added to Repository: Review not attached to Movie")
        if review.review_text is None:
            raise RepositoryException("Review cannot be added to Repository: Review Text Empty")
        if review.rating is None:
            raise RepositoryException("Review cannot be added to Repository: Rating is Empty")

    @abc.abstractmethod
    def get_reviews(self) -> List[Review]:
        """
        Returns List of all Review Objects stored in the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """
        Adds Actor Object to Repository
        """
        if actor.actor_full_name is None:
            raise RepositoryException('Cannot Add Actor to Repository: Actor FullName is None')

    @abc.abstractmethod
    def get_actor(self, fullname):
        """
        Returns Actor Object where the fullname attribute is equal to the fullname parameter provided to the function
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_watchlist(self, watchlist: WatchList):
        """
        Adds Watchlist Object to Repository
        """
        if watchlist.size() == 0:
            raise RepositoryException('Cannot Add WatchList Object to Repository: Watchlist Empty')

    @abc.abstractmethod
    def get_watchlist(self, watchlist: WatchList) -> WatchList:
        """
        Returns Matching WatchList Object from Repository.
        If no match, return None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_watchlists_for_user(self, user: User):
        """
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """
        Adds Director Object to Repository
        """
        if director.director_full_name is None:
            raise RepositoryException("Director cannot be Added to Repository: Fullname is None")

    @abc.abstractmethod
    def get_director_by_name(self, fullname):
        """
        Returns instance of Director object from Repository if Object with fullname attribute found in Repo,
        Otherwise return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """
        Adds Genre to Repository
        """
        if not genre.genre_name:
            raise RepositoryException("Genre cannot be added to the Repository: Genre is None")

    @abc.abstractmethod
    def get_genre(self, target_genre: str):
        """
        Returns instance of genre class from repository if there is an instance with a genre_name attribute equal to
        target_genre otherwise return none
        """
        raise NotImplementedError

    def add_movie_to_watchlist(self, user, movie):
        """
        """
        pass

    def remove_movie_from_watchlist(self, user, movie):
        """
        """
        pass

