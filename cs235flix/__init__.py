import os

from flask import Flask
from cs235flix.cache import cache
import cs235flix.adapters.repository as repo
from cs235flix.adapters.memory_repository import MemoryRepository, populate


def create_app(test_config=None):
    """
    """
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = os.path.join('cs235flix', 'adapters', 'data')
    app.static_folder = 'static'
    cache.init_app(app)

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():
        from .movie import movie
        app.register_blueprint(movie.movie_blueprint)

        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .genre import genre
        app.register_blueprint(genre.genre_blueprint)

        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .person import person
        app.register_blueprint(person.person_blueprint)

        from .watchlist import watchlist
        app.register_blueprint(watchlist.watchlist_blueprint)

        from .search import search
        app.register_blueprint(search.search_bp)

        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)
    return app
