from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, ForeignKeyConstraint
)
from sqlalchemy.orm import mapper, relationship


from cs235flix.domain import model

metadata = MetaData()

users = Table(
    'users',metadata,
    Column('username', String(255), primary_key=True, unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('fullname', String(255), primary_key=True, unique=True, nullable=False),
    Column('has_worked_with',)
)

directors = Table(
    Column('fullname', String(255), primary_key=True, unique=True, nullable=False)
)

genres = Table(
    Column('Name', String(255), primary_key=True, unique=True, nullable=False)
)


movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('release_year', Integer, nullable=False),
    Column('description', String(255), nullable=True),
)


watchlists = Table(

)



reviews = Table(
    'reviews',metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author', ForeignKey('users.username')),
    Column('text', String(255), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False),
)


mapper(model.User, users,properties ={
    '_username': users.c.username,
    '_password': users.c.password,
    '_reviews': relationship(model.Review, backref='_author', order_by=reviews.c.timestamp)
})

mapper(model.Review, reviews, properties={
    '_review_text': reviews.c.text,
    '_rating': reviews.c.rating,
    '_timestamp': reviews.c.timestamp,
})

mapper(model.Movie, movies, properties={
    '_title': movies.c.title,
    '_release_year': movies.c.release_year,
    '_description': movies.c.description,


})



