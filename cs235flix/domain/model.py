import random
from datetime import datetime


class Actor:
    """
    """
    def __init__(self, full_name):
        if full_name == "" or type(full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = full_name.strip()
        self.__has_worked_with = []

    @property
    def actor_full_name(self):
        """
        """
        return self.__actor_full_name

    @property
    def has_worked_with(self):
        """
        """
        return self.__has_worked_with

    def __repr__(self) -> str:
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other) -> bool:
        return self.__actor_full_name == other.actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.actor_full_name

    def __hash__(self) -> int:
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        """
        """
        if colleague not in self.__has_worked_with:
            self.__has_worked_with.append(colleague)
            colleague.add_actor_colleague(self)

    def check_if_this_actor_worked_with(self, colleague):
        """
        """
        return colleague in self.__has_worked_with


class Director:
    """
    """
    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        """
        """
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        if isinstance(other, Director):
            return self.__director_full_name == other.director_full_name
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Director):
            return self.__director_full_name < other.director_full_name
        else:
            return False

    def __hash__(self):
        return hash(self.__director_full_name)


class Genre:
    """
    """
    def __init__(self, genre_name):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name

    @property
    def genre_name(self) -> str:
        """
        """
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if isinstance(other, Genre):
            return self.__genre_name == other.genre_name
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Genre):
            return self.__genre_name < other.genre_name
        else:
            return False

    def __hash__(self):
        return hash(self.__genre_name)


class Movie:
    """
    """
    def __init__(self, title: str, release_year: int):
        if isinstance(title, str):
            title = title.strip()
            if len(title) > 0:
                self.__title = title
        else:
            self.__title = None
        if release_year >= 1900 and isinstance(release_year, int):
            self.__release_year = release_year
        else:
            self.__release_year = None
        self.__description = ""
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = 0
        self.__rank = None
        self.__rating = None
        self.__votes = None
        self.__revenue_in_millions = None
        self.__metascore = None
        self.__reviews = []

    @property
    def title(self) -> str:
        """
        """
        return self.__title

    @title.setter
    def title(self, new_title):
        if isinstance(new_title, str):
            new_title = new_title.strip()
            if len(new_title) > 0:
                self.__title = new_title

    @property
    def release_year(self) -> int:
        """
        """
        return self.__release_year

    @property
    def description(self) -> str:
        """
        """
        return self.__description

    @description.setter
    def description(self, new_description):
        if isinstance(new_description, str) and len(new_description.strip()) > 0:
            self.__description = new_description.strip()

    @property
    def director(self) -> Director:
        """
        """
        return self.__director

    @director.setter
    def director(self, new_director):
        if isinstance(new_director, Director):
            self.__director = new_director

    @property
    def actors(self) -> list:
        """
        """
        if len(self.__actors) > 1:
            for i in range(len(self.__actors)):
                actor1 = self.__actors[i]
                for actor2 in self.__actors[:i] + self.__actors[i + 1:]:
                    actor1.add_actor_colleague(actor2)
        self.__actors.sort()
        return self.__actors

    @actors.setter
    def actors(self, new_actors):
        if isinstance(new_actors, list):
            self.__actors = new_actors

    @property
    def genres(self) -> list:
        """
        """
        self.__genres.sort()
        return self.__genres

    @genres.setter
    def genres(self, new_genres):
        if isinstance(new_genres, list):
            self.__genres = new_genres

    @property
    def runtime_minutes(self) -> int:
        """
        """
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, new_runtime: int):
        if isinstance(new_runtime, int) and new_runtime >= 0:
            self.__runtime_minutes = new_runtime
        else:
            raise ValueError()

    @property
    def rank(self) -> int:
        """
        """
        return self.__rank

    @rank.setter
    def rank(self, new_ranking: int):
        if isinstance(new_ranking, int) and new_ranking > 0:
            self.__rank = new_ranking

    @property
    def rating(self) -> int:
        """
        """
        return self.__rating

    @rating.setter
    def rating(self, new_rating: int):
        if isinstance(new_rating, int) and 10 >= new_rating >= 0:
            self.__rating = new_rating

    @property
    def votes(self):
        """
        """
        return self.__votes

    @votes.setter
    def votes(self, new_votes: int):
        if isinstance(new_votes, int) and new_votes >= 0:
            self.__votes = new_votes

    @property
    def revenue(self):
        """
        """
        return self.__revenue_in_millions

    @revenue.setter
    def revenue(self, new_revenue: float):
        if isinstance(new_revenue, float):
            if new_revenue > 0.0:
                self.__revenue_in_millions = new_revenue

    @property
    def metascore(self):
        """
        """
        return self.__metascore

    @metascore.setter
    def metascore(self, new_metascore: int):
        if isinstance(new_metascore, int) and 0 >= new_metascore <= 100:
            self.__metascore = new_metascore

    @property
    def reviews(self):
        """
        """
        return self.__reviews

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        return (self.__title, self.__release_year) == (other.title, other.release_year)

    def __lt__(self, other):
        return (self.__title, self.__release_year) < (other.title, other.release_year)

    def __hash__(self):
        return hash(self.__title + " " + str(self.__release_year))

    def add_actor(self, actor):
        """
        """
        if isinstance(actor, Actor):
            if actor not in self.__actors:
                self.__actors.append(actor)

    def remove_actor(self, actor):
        """
        """
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre):
        """
        """
        if isinstance(genre, Genre):
            if genre not in self.__genres:
                self.__genres.append(genre)

    def remove_genre(self, genre):
        """
        """
        if genre in self.__genres:
            self.__genres.remove(genre)

    def add_review(self, review):
        """
        """
        if review not in self.__reviews:
            self.__reviews.append(review)

    def remove_review(self, review):
        """
        """
        if review in self.__reviews:
            self.__reviews.remove(review)


class WatchList:
    """
    """
    def __init__(self):
        self.__watchlist = []
        self.__movie_index = -1

    def add_movie(self, movie: Movie):
        """
        """
        if isinstance(movie, Movie) and movie not in self.__watchlist:
            self.__watchlist.append(movie)

    def remove_movie(self, movie: Movie):
        """
        """
        if isinstance(movie, Movie) and movie in self.__watchlist:
            self.__watchlist.remove(movie)

    def select_movie_to_watch(self, index: int):
        """
        """
        if isinstance(index, int) and index in range(len(self.__watchlist)):
            return self.__watchlist[index]
        else:
            return None

    def shuffle_select_movie_to_watch(self):
        """
        """
        return self.__watchlist[random.randint(0, len(self.__watchlist))]

    @property
    def size(self):
        """
        """
        return len(self.__watchlist)

    def first_movie_in_watchlist(self):
        """
        """
        if self.size() != 0:
            return self.__watchlist[0]
        else:
            return None

    def __iter__(self):
        return iter(self.__watchlist)

    def __next__(self):
        self.__movie_index += 1
        if self.__movie_index >= len(self.__watchlist):
            self.__movie_index -= 1
            raise StopIteration
        else:
            return self.__watchlist[self.__movie_index]


class User:
    """
    """

    # noinspection PyPep8Naming
    def __init__(self, user_name: str, password: str, is_admin=False):
        if isinstance(user_name, str) and len(user_name.strip()) > 0:
            self.__user_name = user_name.strip()
            self.__user_name = user_name.lower()
        else:
            self.__user_name = None
        if isinstance(password, str):
            self.__password = password
        else:
            self.__password = None
        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0
        self.__watchlist = WatchList()
        self.__is_admin = is_admin

    def __repr__(self):
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.__user_name == other.user_name
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, User):
            return self.__user_name < other.user_name

    def __hash__(self):
        return hash((self.__user_name, self.__password))

    def watch_movie(self, movie: Movie):
        """
        """
        if isinstance(movie, Movie):
            if movie not in self.__watched_movies:
                self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: object):
        """
        """
        if isinstance(review, Review):
            if review not in self.__reviews:
                self.__reviews.append(review)

    @property
    def user_name(self) -> str:
        """
        """
        return self.__user_name

    @property
    def password(self) -> str:
        """
        """
        return self.__password

    @property
    def watched_movies(self) -> list:
        """
        """
        return self.__watched_movies

    @property
    def reviews(self) -> list:
        """
        """
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        """
        """
        return int(self.__time_spent_watching_movies_minutes)

    @property
    def watchlist(self) -> WatchList:
        """
        """
        return self.__watchlist

    @property
    def is_admin(self) -> bool:
        """
        """
        return self.__is_admin



class Review:
    """
    """
    def __init__(self, movie: Movie, author: User, review_text: str, rating: int):
        if isinstance(movie, Movie):
            self.__movie = movie
        else:
            self.__movie = None
        if isinstance(review_text, str) and len(review_text.strip()) > 0:
            self.__review_text = review_text.strip()
        else:
            self.__review_text = None
        if isinstance(rating, int) and 10 >= rating >= 1:
            self.__rating = rating
        else:
            self.__rating = None

        self.__timestamp = datetime.today()
        self.__author = author

    def __eq__(self, other):
        if isinstance(other, Review):
            return (self.__movie, self.__review_text, self.__rating, self.__timestamp) == (
                other.movie, other.review_text, other.rating, other.timestamp)
        else:
            return False

    def __repr__(self):
        return f"<Review {self.__movie}, {self.__review_text}, {self.__rating}, {self.__timestamp}>"

    def __hash__(self):
        return hash((self.__movie, self.__review_text, self.__rating, self.__timestamp))

    @property
    def movie(self):
        """
        """
        return self.__movie

    @property
    def review_text(self):
        """
        """
        return self.__review_text

    @property
    def rating(self):
        """
        """
        return self.__rating

    @property
    def timestamp(self):
        """
        """
        return self.__timestamp

    @property
    def author(self):
        """
        """
        return self.__author


class UserGroup:
    """
    """
    def __init__(self, owner: User, name=None):
        if name is None or len(name.strip()) == 0 or not isinstance(name, str):
            self.__group_name = "New Group"
        else:
            self.__group_name = name.strip()
        self.__owner = owner
        self.__members = [owner]
        self.__watchlist = WatchList()

    def __repr__(self) -> str:
        return f"<UserGroup {self.__group_name}>"

    def __eq__(self, other):
        if isinstance(other, UserGroup):
            return (self.__owner, self.__members) == (other.__owner, other.__members)

    def __hash__(self):
        return hash((self.__group_name, self.__owner, self.__members))

    @property
    def group_name(self) -> str:
        """
        """
        return self.__group_name

    @group_name.setter
    def group_name(self, new_name):
        if new_name and len(new_name.strip()) > 0 and isinstance(new_name, str):
            self.__group_name = new_name.strip()
            self.__watchlist.name = f'{self.__group_name}\'s WatchList'

    @property
    def owner(self) -> User:
        """
        """
        return self.__owner

    @property
    def watchlist(self):
        """
        """
        return self.__watchlist

    @property
    def members(self):
        """
        """
        return self.__members

    def watch_movie(self, movie):
        """
        """
        for user in self.__members:
            user.watch_movie(movie)

    def add_member(self, user: User):
        """
        """
        if isinstance(user, User) and user not in self.__members:
            if self.__owner != user:
                self.__members.append(user)

    def remove_member(self, user: User):
        """
        """
        if isinstance(user, User) and user in self.__members:
            if self.__owner != user:
                self.__members.remove(user)

    def is_member(self, user: User):
        """
        """
        if isinstance(user, User):
            return user in self.__members


class ModelException(Exception):
    """
    """

    # noinspection PyUnusedLocal
    def __init__(self, message=None):
        pass


def make_review(user, movie, review_text, rating):
    """
    """
    review = Review(movie, user, review_text, rating)
    user.add_review(review)
    movie.add_review(review)
    return review


def add_to_watchlist(user, movie):
    """
    """
    user.watchlist.add_movie(movie)
    return user.watchlist
