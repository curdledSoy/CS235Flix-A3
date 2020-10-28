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
        if not self.__session is None:
            self.__session.close()

class SQLAlchemyRepository(AbstractRepository):
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
        super().add_user(user)
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
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
            movie = self._session_cm.session.query(Movie).filter(Movie._title == title and Movie._release_year == year).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_movies_by_year(self, target_year: date) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).filter(Movie._release_year == target_year).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_title(self, title: str) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).filter(Movie._title == title).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_director(self, director: Director) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.query(Movie).filter(Movie._director.fullname == director.director_full_name).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_actor(self, actor: Actor) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.query(Movie).filter(Movie._actor.fullname == actor.actor_full_name).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_genre(self, genre: Genre) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.query(Movie).filter(Movie._genre.name == genre.genre_name).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_rating(self, rating: int) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.query(Movie).filter(Movie._rating == rating).all()
        except NoResultFound:
            pass

        return movies

    def get_movies_by_rank(self) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.query(Movie).order_by(asc(Movie._rank)).all()
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
            group = self._session_cm.query(UserGroup).filter(UserGroup._name == groupname).one()
        except NoResultFound:
            pass

        return group

    def get_user_groups(self, user: User) -> List[UserGroup]:
        groups = None
        try:
            groups = self._session_cm.query(UserGroup).all()
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
            reviews = self._session_cm.query(Review).all()
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
            actor = self._session_cm.session.query(Actor).filter_by(Actor._name == fullname).one()
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
            director = self._session_cm.session.query(Director).filter_by(Director._name == fullname).one()
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


def read_csv(filename: str):
    """
    """
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)

        headers = next(reader)

        for row in reader:
            row = [cell.strip() for cell in row]
            yield row

def load_movies(data_path: str):
    for data_row in read_csv(os.path.join(data_path, 'Data1000Movies.csv')):
        movie = Movie(data_row[1], int(data_row[6]))
        movie.rank = int(data_row[0])
        movie.genres = load_genres(data_row[2])
        movie.description = data_row[3]
        movie.director = load_directors(data_row[4])
        movie.actors = load_actors(data_row[5])
        try:
            movie.runtime_minutes = int(data_row[7])
        except ValueError:
            movie.runtime_minutes = 0
        try:
            movie.rating = int(data_row[8])
        except ValueError:
            pass
        try:
            movie.votes = int(data_row[9])
        except ValueError:
            pass
        try:
            movie.revenue = float(data_row[10])
        except ValueError:
            pass
        try:
            movie.metascore = int(data_row[11])
        except ValueError:
            pass

        movie_data = {
            'title': data_row[1],
            'year': int(data_row[6]),
            'rank': movie.rank,
            'genres': movie.genres,
            'description': movie.description,
            'director': movie.director,
            'actors': movie.actors,
        }

        yield movie_data




def load_actors(actors: str):
    """
    """
    names = actors.split(',')
    movie_actors = []
    for name in names:
        temp_actor = Actor(name)
        if temp_actor not in movie_actors:
            movie_actors.append(temp_actor)
        if temp_actor not in actors:
            actors.add(temp_actor)
    return movie_actors


def load_genres(genres: str):
    """
    """
    genres_as_str = genres.split(',')
    movie_genres = []
    for genre in genres_as_str:
        temp_genre = Genre(genre)
        if temp_genre not in movie_genres:
            movie_genres.append(temp_genre)
        if temp_genre not in genres:
            genres.add(temp_genre)
    return movie_genres


def load_directors(director: str):
    """
    """
    temp_director = Director(director)
    if temp_director not in directors:
        directors.add(temp_director)
    return temp_director


def load_users(data_path):
    """
    """
    users = dict()
    for data_row in read_csv(os.path.join(data_path, 'Users.csv')):
        user = User(
            data_row[0],
            generate_password_hash(data_row[1])
        )
        users[data_row[0]] = user
    return users


def populate(data_path: str, repo: SQLAlchemyRepository):
    conn = engine.raw_connection()
    cursor = conn.cursor()


    global directors
    directors = set()

    global actors
    actors = set()

    global genres
    genres = set()

    insert_movies = """
        INSERT INTO movies (
        title, year, rank, rating, description, runtime, votes, revenue, metascore )
        VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, load_movies(data_path))

    conn.commit()
    conn.close()