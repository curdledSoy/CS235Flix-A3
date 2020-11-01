import csv
import os
from typing import List, Optional
from werkzeug.security import generate_password_hash
from .repository import AbstractRepository, RepositoryException
from ..domain.model import Director, WatchList, Actor, Movie, Review, User, UserGroup, Genre
from .MovieFileReader import MovieFileReader

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__actors = set()
        self.__directors = set()
        self.__genres = set()
        self.__movies: List[Movie] = []
        self.__users = []
        self.__watchlists = []
        self.__reviews = set()
        self.__userGroups = []

    @property
    def dataset_of_movies(self):

        return self.__movies

    @dataset_of_movies.setter
    def dataset_of_movies(self, movies):
        self.__movies = movies

    @property
    def dataset_of_actors(self):
        return self.__actors

    @dataset_of_actors.setter
    def dataset_of_actors(self, actors):
        self.__actors = actors

    @property
    def dataset_of_directors(self):

        return self.__directors

    @dataset_of_directors.setter
    def dataset_of_directors(self, directors):
        self.__directors = directors

    @property
    def dataset_of_genres(self):

        return self.__genres

    @dataset_of_genres.setter
    def dataset_of_genres(self, genres):
        self.__genres = genres

    @property
    def dataset_of_users(self):

        return self.__users

    @dataset_of_users.setter
    def dataset_of_users(self, users):
        self.__users = users

    @property
    def dataset_of_groups(self):

        return self.__userGroups

    @property
    def dataset_of_reviews(self):

        return self.__reviews

    @property
    def dataset_of_watchlists(self):

        return self.__watchlists

    def add_user(self, user: User):
        """
        """
        if user not in self.__users:
            self.__users.append(user)
            self.__watchlists.append(user.watchlist)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.user_name == username.lower()), None)

    # noinspection PyUnusedLocal
    def add_movie(self, movie: Movie):
        """
        """
        try:
            super().add_movie(movie)
            self.__movies.append(movie)
        except RepositoryException as e:
            pass

    def get_movie(self, title: str, year: int) -> Movie:
        """
        """
        return next((movie for movie in self.__movies if movie.title == title and movie.release_year == year), None)

    def get_movies_by_year(self, target_year: int) -> Optional[List[Movie]]:
        """
        """
        try:
            matching_movies = []
            for movie in self.__movies:
                if movie.release_year == target_year:
                    matching_movies.append(movie)
            if len(matching_movies) > 0:
                return matching_movies
            else:
                return None
        except ValueError:
            return None

    def get_movies_by_title(self, target_title: str) -> Optional[List[Movie]]:
        """
        """
        try:
            matching_movies = []
            for movie in self.__movies:
                if movie.title == target_title:
                    matching_movies.append(movie)
            if len(matching_movies) > 0:
                return matching_movies
            else:
                return None
        except ValueError:
            return None

    def get_movies_by_director(self, target_director: Director) -> Optional[List[Movie]]:
        """
        """
        try:
            matching_movies = []
            for movie in self.__movies:
                if movie.director.director_full_name == target_director.director_full_name:
                    matching_movies.append(movie)
            if len(matching_movies) > 0:
                return sorted(matching_movies)
            else:
                return None
        except ValueError:
            return None

    def get_movies_by_actor(self, target_actor: Actor) -> Optional[List[Movie]]:
        """
        """
        try:
            matching_movies = []
            for movie in self.__movies:
                if target_actor in movie.actors:
                    matching_movies.append(movie)
            if len(matching_movies) > 0:
                return matching_movies
            else:
                return None
        except ValueError:
            return None

    def get_movies_by_genre(self, target_genre: Genre) -> Optional[List[Movie]]:
        """
        """
        try:
            matching_movies = []
            for movie in self.__movies:
                if target_genre in movie.genres:
                    matching_movies.append(movie)
            if len(matching_movies) > 0:
                return matching_movies
            else:
                return None
        except ValueError:
            return None

    def get_movies_by_rating(self, target_rating: int) -> Optional[List[Movie]]:
        """
        """
        try:
            matching_movies = []
            for movie in self.__movies:
                if movie.rating >= target_rating:
                    matching_movies.append(movie)
            if len(matching_movies) > 0:
                return matching_movies
            else:
                return None
        except ValueError:
            return None

    def get_movies_by_rank(self) -> List[Movie]:
        """
        """
        return sorted(self.__movies, key=lambda x: x.rank)

    def add_group(self, group: UserGroup):
        """
        """
        super().add_group(group)
        self.__userGroups.append(group)
        self.__watchlists.append(group.watchlist)

    def get_group(self, groupname) -> UserGroup:
        """
        """
        return next((group for group in self.__userGroups if group.group_name == groupname))

    def get_user_groups(self, user: User) -> Optional[list]:
        """
        """
        try:
            matching_groups = []
            for group in self.__userGroups:
                if group.is_member(user):
                    matching_groups.append(group)
            if len(matching_groups) == 0:
                return None
            else:
                return sorted(matching_groups, key=lambda x: x.group_name)
        except ValueError:
            return None

    def add_review(self, review: Review):
        """
        """
        super().add_review(review)
        self.__reviews.add(review)

    def get_reviews(self) -> List[Review]:
        """
        """
        return list(self.__reviews)

    def add_actor(self, actor: Actor):
        """
        """
        super().add_actor(actor)
        if actor not in self.__actors:
            self.__actors.add(actor)

    def get_actor(self, fullname):
        """
        """
        matching_actor = None
        for actor in self.__actors:
            if actor.actor_full_name == fullname:
                matching_actor = actor
                break
        return matching_actor

    def add_watchlist(self, watchlist: WatchList):
        """
        """
        super().add_watchlist(watchlist)
        self.__watchlists.append(watchlist)

    def get_watchlist(self, target_watchlist: WatchList) -> WatchList:
        """
        """
        return next((watchlist for watchlist in self.__watchlists if watchlist == target_watchlist))

    def get_watchlists_for_user(self, user: User):
        """
        """
        if user in self.__users:
            return user.watchlist
        else:
            return None

    def add_director(self, director: Director):
        """
        """
        super().add_director(director)
        self.__directors.add(director)

    def get_director_by_name(self, fullname):
        """
        """
        matching_director = None
        for director in self.__directors:
            if director.director_full_name == fullname:
                matching_director = director
                break
        return matching_director

    def add_genre(self, genre: Genre):
        """
        """
        if isinstance(genre, Genre) and genre not in self.__genres:
            self.__genres.add(genre)

    def get_genre(self, target_genre: str):
        """
        """
        if Genre(target_genre) in self.__genres:
            return Genre(target_genre)
        else:
            return None

    def add_movie_to_watchlist(self, entity: User or UserGroup, movie: Movie):
        """
        """
        for user in self.dataset_of_users:
            if user == entity:
                user.watchlist.add_movie(movie)

    def remove_movie_from_watchlist(self, entity: User or UserGroup, movie: Movie):
        """
        """
        for user in self.dataset_of_users:
            if user == entity:
                user.watchlist.remove_movie(movie)



def populate(data_path: str, repo: MemoryRepository):
    movieFileReader = MovieFileReader(data_path)
    repo.dataset_of_genres = MovieFileReader.dataset_of_genres
    repo.dataset_of_directors = MovieFileReader.dataset_of_directors
    repo.dataset_of_actors = MovieFileReader.dataset_of_actors
    repo.dataset_of_users = MovieFileReader.dataset_of_users
    repo.dataset_of_movies = MovieFileReader.dataset_of_movies
