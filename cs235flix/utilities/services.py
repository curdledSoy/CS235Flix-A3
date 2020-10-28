from datetime import datetime

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import Movie, Review


def movie_to_dict(movie: Movie):
    """
    """
    movie_dict = dict(rank=movie.rank, title=movie.title, year=movie.release_year, runtime=movie.runtime_minutes,
                      actors=[actor.actor_full_name for actor in movie.actors],
                      director=movie.director.director_full_name, genres=[genre.genre_name for genre in movie.genres],
                      description=movie.description, rating=movie.rating, votes=movie.votes, revenue=movie.revenue,
                      meta_score=movie.metascore)
    return movie_dict


def get_user_watchlist(username: str, repo: AbstractRepository):
    """
    """
    watchlist = repo.get_watchlists_for_user(repo.get_user(username=username))
    if watchlist and watchlist.size() != 0:
        return [movie_to_dict(movie) for movie in watchlist]
    else:
        return []


def reviews_to_dict(reviews):
    """
    """
    return sorted([review_to_dict(review) for review in reviews], reverse=True, key=lambda x: x['timestamp'])


def review_to_dict(review: Review):
    """
    """
    review_dict = dict(author=review.author.user_name,
                       review_text=review.review_text,
                       rating=review.rating,
                       movie_title=review.movie.title,
                       movie_year=review.movie.release_year,
                       )
    if datetime.today().strftime('%m/%d/%Y') == review.timestamp.strftime('%m/%d/%Y'):
        review_dict['timestamp'] = review.timestamp.strftime('%H:%M')
    else:
        review_dict['timestamp'] = review.timestamp.strftime('%d/%m')
    return review_dict
