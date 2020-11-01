import csv
import os
from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from cs235flix.adapters.MovieFileReader import MovieFileReader
from cs235flix.domain.model import User, Movie, Review, Actor, Director, UserGroup, Genre, WatchList
from cs235flix.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    @property
    def dataset_of_movies(self):
        movies = self._session_cm.session.query(Movie).all()
        return movies

    @property
    def dataset_of_actors(self):
        actors = self._session_cm.session.query(Actor).all()
        return actors

    @property
    def dataset_of_directors(self):
        directors = self._session_cm.session.query(Director).all()
        return directors

    @property
    def dataset_of_genres(self):
        genres = self._session_cm.session.query(Genre).all()
        return genres

    @property
    def dataset_of_users(self):
        users = self._session_cm.session.query(User).all()
        return users

    @property
    def dataset_of_groups(self):
        groups = self._session_cm.session.query(UserGroup).all()
        return groups

    @property
    def dataset_of_reviews(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    @property
    def dataset_of_watchlists(self):
        watchlists = self._session_cm.session.query(WatchList).all()
        return watchlists

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(User.__user_name == username).one()
        except NoResultFound:
            pass

        return user

    def add_movie(self, movie: Movie):
        super().add_movie(movie)
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, title: str, year: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(
                Movie.__title == title and Movie.__release_year == year).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_movies_by_year(self, target_year: date) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).filter(Movie.__release_year == target_year).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_title(self, title: str) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).filter(Movie.__title == title).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_director(self, director: Director) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).filter(director == Movie.__director).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_actor(self, actor: Actor) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).filter(actor in Movie.__actors).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_genre(self, genre: Genre) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).filter(Movie.__genre.__name == genre.genre_name).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_rating(self, rating: int) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).filter(Movie.rating == rating).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_rank(self) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).all()
        except NoResultFound:
            pass

        return movies

    def add_group(self, group: UserGroup):
        super().add_group(group)
        with self._session_cm as scm:
            scm.session.add(group)
            scm.commit()

    def get_group(self, groupname) -> UserGroup:
        group = None
        try:
            group = self._session_cm.session.query(UserGroup).filter(UserGroup.group_name == groupname).one()
        except NoResultFound:
            pass

        return group

    def get_user_groups(self, user: User) -> List[UserGroup]:
        groups = None
        try:
            groups = self._session_cm.session.query(UserGroup).all()
            for group in groups:
                if user not in group:
                    groups.remove(group)
        except NoResultFound:
            pass

        return groups

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self) -> List[Review]:
        reviews = None
        try:
            reviews = self._session_cm.session.query(Review).all()
        except NoResultFound:
            pass

        return reviews

    def add_actor(self, actor: Actor):
        super().add_actor(actor)
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def get_actor(self, fullname):
        actor = None
        try:
            actor = self._session_cm.session.query(Actor).filter_by(Actor.actor_full_name == fullname).one()
        except NoResultFound:
            pass

        return actor

    def add_watchlist(self, watchlist: WatchList):
        super().add_watchlist(watchlist)
        with self._session_cm as scm:
            scm.session.add(watchlist)
            scm.commit()

    def get_watchlist(self, watchlist: WatchList) -> WatchList:
        pass

    def get_watchlists_for_user(self, user: User):
        pass

    def add_director(self, director: Director):
        super().add_director(director)
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def get_director_by_name(self, fullname):
        director = None
        try:
            director = self._session_cm.session.query(Director).filter_by(Director.director_full_name == fullname).one()
        except NoResultFound:
            pass

        return director

    def add_genre(self, genre: Genre):
        super().add_genre(genre)
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_genre(self, target_genre: str):
        pass


def user_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)
        id = 1
        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            row = [id] + row
            id += 1

            yield row


def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        director_id = 0
        movie_key = 0
        # Read remaining rows from the CSV file.
        for row in reader:
            director_id += 1
            movie_data = row
            movie_key += 1

            # Strip any leading/trailing white space from data read.
            movie_data = [item.strip() for item in movie_data]

            movie_genres = movie_data[2].split(',')
            movie_actors = movie_data[5].split(',')
            movie_director = movie_data[4]
            # Add any new GENRES; associate the current article with tags.
            for genre in movie_genres:
                if genre not in genres.keys():
                    genres[genre] = list()
                genres[genre].append(movie_key)

            for actor in movie_actors:
                if actor not in actors.keys():
                    actors[actor] = list()
                actors[actor].append(movie_key)

            if movie_director not in directors.keys():
                directors[movie_director] = dict(id=director_id, movies=[])
            directors[movie_director]['movies'].append(movie_key)

            yield movie_key, movie_data[1], movie_data[6], movie_data[3], movie_data[7], movie_data[0], movie_data[8], \
                  movie_data[9], movie_data[10], movie_data[11], director_id


def get_genre_records():
    genre_records = list()
    genre_key = 0

    for genre in genres.keys():
        genre_key += 1
        genre_records.append((genre_key, genre))

    return genre_records


def movie_genres_generator():
    movie_genres_key = 0
    genre_key = 0

    for genre in genres.keys():
        genre_key += 1
        for movie_key in genres[genre]:
            movie_genres_key += 1
            yield movie_genres_key, movie_key, genre_key


def get_actor_records():
    actor_records = list()
    actor_key = 0

    for actor in actors.keys():
        actor_key += 1
        actor_records.append((actor_key, actor))

    return actor_records


def movie_actors_generator():
    movie_actor_key = 0
    actor_key = 0

    for actor in actors.keys():
        actor_key += 1
        for movie_key in actors[actor]:
            movie_actor_key += 1
            yield movie_actor_key, movie_key, actor_key


def get_director_records():
    director_records = list()

    for director in directors.keys():
        director_records.append((directors[director]['id'], director))
        print(director)
    return director_records


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    global genres
    genres = dict()

    global actors
    actors = dict()

    global directors
    directors = dict()

    insert_movies = """
        INSERT INTO movies (
        id, title, release_year, description, runtime_minutes, rank, votes, revenue, metascore, director_id)
        VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, 'Data1000Movies.csv')))

    insert_genres = """
        INSERT INTO genres (
        id, genre_name)
        VALUES (?, ?)"""
    cursor.executemany(insert_genres, get_genre_records())

    insert_movie_genres = """
        INSERT INTO movie_genres (
        id, movie_id, genre_id)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_genres, movie_genres_generator())

    insert_actors = """
        INSERT INTO actors (
        id, actor_full_name)
        VALUES (?, ?)"""
    cursor.executemany(insert_actors, get_actor_records())

    insert_movie_actors = """
            INSERT INTO movie_actors (
            id, movie_id, actor_id)
            VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_actors, movie_actors_generator())

    insert_directors = """
        INSERT INTO directors (
        id, director_full_name)
        VALUES (?, ?)"""
    cursor.executemany(insert_directors, get_director_records())

    insert_users = """
        INSERT INTO users (
        id, user_name, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, user_generator(os.path.join(data_path, 'users.csv')))

    conn.commit()
    conn.close()
