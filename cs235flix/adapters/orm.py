from sqlalchemy import (
    Table, MetaData, Column, Integer, Text, String, Date, DateTime,
    ForeignKey, ForeignKeyConstraint, Boolean, Float, Numeric
)
from sqlalchemy.orm import mapper, relationship, collections, backref

from cs235flix.domain import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('time_spent_watching_movies_minutes', Integer, nullable=True),
    Column('is_admin', Boolean, nullable=True),
    Column('watchlist_id', ForeignKey('watchlists.id')),
    Column('watched_movies', ForeignKey('movies.id')),
)
reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('text', Text, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('movie_id', ForeignKey('movies.id'))
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('actor_full_name', String(255), unique=True, nullable=False),
)

actor_colleagues = Table(
    'actor_colleagues', metadata,
    Column('actor_id', ForeignKey('actors.id')),
    Column('colleague_id', ForeignKey('actors.id'))
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('director_full_name', String(255), unique=True, nullable=True)
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('actor_id', ForeignKey('actors.id')),
    Column('movie_id', ForeignKey('movies.id'))
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('genre_name', String(255), unique=True, nullable=False)
)
movie_genres = Table(
    'movie_genres', metadata,
    Column('genre_id', ForeignKey('genres.id')),
    Column('movie_id', ForeignKey('movies.id'))
)
movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('release_year', Integer, nullable=False),
    Column('description', String(255), nullable=True),
    Column('runtime_minutes', Integer, nullable=True),
    Column('rank', Integer, nullable=True),
    Column('rating', Integer, nullable=True),
    Column('votes', Integer, nullable=True),
    Column('revenue', Float, nullable=True),
    Column('metascore', Integer, nullable=True),
    Column('director_id', ForeignKey('directors.id'), nullable=True)
)

watchlists = Table(
    'watchlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('size', Integer, nullable=True),
    Column('index', Numeric, nullable=True),
)

watchlist_movies = Table(
    'watchlist_movie_association', metadata,
    Column('watchlist_id', ForeignKey('watchlists.id')),
    Column('movie_id', ForeignKey('movies.id'))
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_User__user_name': users.c.user_name,
        '_User__password': users.c.password,
        '_User__time_spent_watching_movies_minutes': users.c.time_spent_watching_movies_minutes,
        '_User__is_admin': users.c.is_admin,
        '_User__reviews': relationship(model.Review, backref='_Review__author', order_by=reviews.c.timestamp),
        '_User__watched_movies': relationship(model.Movie),
        '_User__watchlist': relationship(model.WatchList, uselist=False)
    })

    mapper(model.Review, reviews, properties={
        '_Review__review_text': reviews.c.text,
        '_Review__rating': reviews.c.rating,
        '_Review__timestamp': reviews.c.timestamp,

    })
    genres_mapper = mapper(model.Genre, genres, properties={
        '_Genre__genre_name': genres.c.genre_name
    })

    actors_mapper = mapper(model.Actor, actors, properties={
        '_Actor__actor_full_name': actors.c.actor_full_name,
        '_Actor__has_worked_with': relationship(model.Actor, secondary=actor_colleagues,
                                                primaryjoin=actors.c.id == actor_colleagues.c.actor_id,
                                                secondaryjoin=actors.c.id == actor_colleagues.c.colleague_id)
    })

    movie_mapper = mapper(model.Movie, movies, properties={
        '_Movie__title': movies.c.title,
        '_Movie__release_year': movies.c.release_year,
        '_Movie__rank': movies.c.rank,
        '_Movie__rating': movies.c.rating,
        '_Movie__description': movies.c.description,
        '_Movie__votes': movies.c.votes,
        '_Movie__revenue': movies.c.revenue,
        '_Movie__metascore': movies.c.metascore,
        '_Movie__reviews': relationship(model.Review, backref='_Review__movie', order_by=reviews.c.timestamp),
        '_Movie__actors': relationship(actors_mapper, secondary=movie_actors),
        '_Movie__genres': relationship(genres_mapper, secondary=movie_genres),
        '_Movie__director': relationship(model.Director),
    })

    mapper(model.Director, directors, properties={
        '_Director__director_full_name': directors.c.director_full_name,
    })

    mapper(model.WatchList, watchlists, properties={
        '_Watchlist__movie_index': watchlists.c.index,
        '_Watchlist__size': watchlists.c.size,
        '_Watchlist__watchlist': relationship(movie_mapper, secondary=watchlist_movies)
    })
