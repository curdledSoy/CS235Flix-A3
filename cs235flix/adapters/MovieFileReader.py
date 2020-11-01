import csv
import os
from typing import List

from werkzeug.security import generate_password_hash

from ..domain.model import Director, User, Genre, Actor, Movie


class MovieFileReader:
    def __init__(self, datapath):
        self.__actors = set()
        self.__directors = set()
        self.__genres = set()
        self.__movies: List[Movie] = []
        self.__users = []
        self.__watchlists = []
        self.load_movies(datapath)
        self.load_users(datapath)

    @property
    def dataset_of_movies(self):

        return self.__movies

    @property
    def dataset_of_actors(self):

        return self.__actors

    @property
    def dataset_of_directors(self):
        return self.__directors

    @property
    def dataset_of_genres(self):
        return self.__genres

    @property
    def dataset_of_users(self):
        return self.__users

    @property
    def dataset_of_watchlists(self):
        return self.dataset_of_watchlists


    def read_csv(self, filename: str):
        with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)

            headers = next(reader)

            for row in reader:
                row = [cell.strip() for cell in row]
                yield row

    def load_movies(self, data_path: str):
        for data_row in self.read_csv(os.path.join(data_path, 'Data1000Movies.csv')):
            movie = Movie(data_row[1], int(data_row[6]))
            movie.rank = int(data_row[0])
            movie.genres = self.load_genres(data_row[2])
            movie.description = data_row[3]
            movie.director = self.load_directors(data_row[4])
            movie.actors = self.load_actors(data_row[5])
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

            if movie not in self.dataset_of_movies:
                self.__movies.append(movie)

    def load_actors(self, actors: str, ):
        names = actors.split(',')
        actors = []
        for name in names:
            temp_actor = Actor(name)
            if temp_actor not in actors:
                actors.append(temp_actor)
            if temp_actor not in self.dataset_of_actors:
                self.__actors.add(temp_actor)
        return actors

    def load_genres(self, genres: str):
        genres_as_str = genres.split(',')
        genres = []
        for genre in genres_as_str:
            temp_genre = Genre(genre)
            if temp_genre not in genres:
                genres.append(temp_genre)
            if temp_genre not in self.dataset_of_genres:
                self.__genres.add(temp_genre)
        return genres

    def load_directors(self, director: str):
        temp_director = Director(director)
        if temp_director not in self.dataset_of_directors:
            self.__directors.add(temp_director)
        return temp_director

    def load_users(self, data_path):
        users = dict()
        for data_row in self.read_csv(os.path.join(data_path, 'Users.csv')):
            user = User(
                data_row[0],
                generate_password_hash(data_row[1])
            )
            self.__users.append(user)
            self.__watchlists.append(user.watchlist)
            users[data_row[0]] = user
        return users
